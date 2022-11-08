import pytest
from src.ssg import create_posts, render_home, render_posts, render_tags
from jinja2 import Environment, FileSystemLoader
import pathlib
from datetime import datetime
import tempfile
import shutil


@pytest.fixture
def test_setup():

    # write md contents

    tmp_dir = tempfile.mkdtemp()
    root_path = pathlib.Path(tmp_dir)
    prototypes_path = root_path.joinpath("prototypes").resolve()
    prototypes_path.mkdir(mode=511, parents=True, exist_ok=True)
    test_md = prototypes_path.joinpath("test.md").resolve()
    with open(test_md, "w") as f:
        f.write("title: test\n")
        f.write("date: " + f"{datetime.today().strftime('%d-%m-%Y')}\n")
        f.write("tags: test\n")
        f.write("name: test\n")
        f.write("summary: test\n")
        f.write("-------------\n")
        f.write("\n")
        f.write("#test header\n")
        f.write("test content")

    # write test config.yml
    config_path = root_path.joinpath("config.yml").resolve()
    with open(config_path, "w") as f:
        f.write("github: github.com\n")
        f.write("stackoverflow: stackoverflow.com\n")
        f.write("linkedin: linkedin.com\n")
        f.write("email: email@email.com\n")
        f.write("resume: resume.pdf\n")
        f.write("profile_picture: my_profile.png\n")
        f.write("blog_title: test blog\n")

    yield root_path

    # tear down
    shutil.rmtree(root_path.resolve())  # rm all files in mkdtemp


def test_create_posts(test_setup):

    path = test_setup

    test_metadata = [
        {
            "title": "test",
            "date": f"{datetime.today().strftime('%d-%m-%Y')}",
            "tags": ["test"],
            "name": "test",
            "summary": "test",
        }
    ]
    test_post = {"test.md": "<h1>test header</h1>\n\n<p>test content</p>\n"}
    test_tags = {"test"}
    test_info = {
        "github": "github.com",
        "stackoverflow": "stackoverflow.com",
        "linkedin": "linkedin.com",
        "email": "email@email.com",
        "resume": "resume.pdf",
        "profile_picture": "my_profile.png",
        "blog_title": "test blog",
    }

    posts, metadata, tags, info = create_posts(path.resolve())

    assert posts == test_post
    assert metadata == test_metadata
    assert tags == test_tags
    assert info == test_info


def test_render_home(test_setup):
    path = test_setup

    # mk tests folder

    _, metadata, tags, info = create_posts(path.resolve())
    env = Environment(loader=FileSystemLoader(searchpath="./src/templates"))
    home_template = env.get_template("home.html")

    render_home(metadata, path.resolve(), tags, home_template, info)

    # test_index_content
    with open(path.joinpath("index.html"), "r") as f:
        index_content = f.read()

    test_index_content = f"""<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <link rel="stylesheet" href="../static/main.css" />\n    <link\n      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"\n      rel="stylesheet"\n      integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU"\n      crossorigin="anonymous"\n    />\n\n    <link\n      rel="stylesheet"\n      href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/base16/solarized-light.min.css"\n      integrity="sha512-ZW2g6Pn2pMbKSyjcA+r4Lc58kcfvOdcsTuCCTl3qz8NqVJwUtAuiN61pDoW3EEfrjwH2CPtkFWMdkzMY1idilA=="\n      crossorigin="anonymous"\n      referrerpolicy="no-referrer"\n    />\n    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>\n    <link\n      rel="stylesheet"\n      href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css"\n      integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p"\n      crossorigin="anonymous"\n    />\n    <link\n      href="https://fonts.googleapis.com/css?family=Inter"\n      rel="stylesheet"\n      crossorigin="anonymous"\n    />\n\n    <title>test blog</title>\n  </head>\n  <body>\n    <div class="main">\n      <div class="heading">\n        <a href="/"\n          ><img\n            id="home-icon"\n            src="my_profile.png"\n            alt="Python Trioxide"\n        /></a>\n        <div class="info">\n          <a href="github.com" title="Github">\n            <i class="fab fa-github-alt"></i\n          ></a>\n          <a href="stackoverflow.com" title="Stack Overflow"\n            ><i class="fab fa-stack-overflow"></i\n          ></a>\n          <a href="linkedin.com" title="LinkedIn"\n            ><i class="fab fa-linkedin"></i\n          ></a>\n          <a href="mailto: email@email.com" title="Email"\n            ><i class="fas fa-at"></i\n          ></a>\n          <a href="resume.pdf" title="Resume"\n            ><i class="fas fa-file"></i\n          ></a>\n        </div>\n      </div>\n      <div id="container">\n        \n<h1>Tất cả các bài viết</h1><br>\n\n\n  <p>\n    <div class="home-summ">\n      <small class="home-meta">{datetime.today().strftime('%d-%m-%Y')}</small>\n      <br>\n      <small class="home-meta right">\n        tags: \n         \n          <a href="tags/test.html" id="link-tags">test</a>\n        \n      </small>\n    </div>\n    <h3>\n      <a href="../posts/test.html" id="link-post">\n        test\n      </a>\n    </h3>\n    <small>\n      test\n    </small>\n  </p>\n\n \n      </div>\n    </div>\n    <script src="../static/script.js" type="text/javascript"></script>\n  </body>\n</html>"""  # check file index.html is exists
    # print(repr(index_content))
    assert path.joinpath("index.html").exists() == True
    assert test_index_content == index_content


def test_render_posts(test_setup):
    path = test_setup

    # create posts folder in temp folder
    path.joinpath("posts/").mkdir(mode=511, parents=True, exist_ok=True)

    posts, _, tags, info = create_posts(root_path=path.resolve())
    env = Environment(loader=FileSystemLoader(searchpath="./src/templates"))
    post_html = env.get_template("post.html")

    render_posts(
        posts,
        tags,
        path.joinpath("posts").resolve(),
        post_html,
        info,
    )

    with open(path.joinpath("posts/test.html"), "r") as f:
        post_content = f.read()

    test_post_content = f"""<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <link rel="stylesheet" href="../static/main.css" />\n    <link\n      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"\n      rel="stylesheet"\n      integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU"\n      crossorigin="anonymous"\n    />\n\n    <link\n      rel="stylesheet"\n      href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/base16/solarized-light.min.css"\n      integrity="sha512-ZW2g6Pn2pMbKSyjcA+r4Lc58kcfvOdcsTuCCTl3qz8NqVJwUtAuiN61pDoW3EEfrjwH2CPtkFWMdkzMY1idilA=="\n      crossorigin="anonymous"\n      referrerpolicy="no-referrer"\n    />\n    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>\n    <link\n      rel="stylesheet"\n      href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css"\n      integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p"\n      crossorigin="anonymous"\n    />\n    <link\n      href="https://fonts.googleapis.com/css?family=Inter"\n      rel="stylesheet"\n      crossorigin="anonymous"\n    />\n\n    <title>test blog</title>\n  </head>\n  <body>\n    <div class="main">\n      <div class="heading">\n        <a href="/"\n          ><img\n            id="home-icon"\n            src="my_profile.png"\n            alt="Python Trioxide"\n        /></a>\n        <div class="info">\n          <a href="github.com" title="Github">\n            <i class="fab fa-github-alt"></i\n          ></a>\n          <a href="stackoverflow.com" title="Stack Overflow"\n            ><i class="fab fa-stack-overflow"></i\n          ></a>\n          <a href="linkedin.com" title="LinkedIn"\n            ><i class="fab fa-linkedin"></i\n          ></a>\n          <a href="mailto: email@email.com" title="Email"\n            ><i class="fas fa-at"></i\n          ></a>\n          <a href="resume.pdf" title="Resume"\n            ><i class="fas fa-file"></i\n          ></a>\n        </div>\n      </div>\n      <div id="container">\n        \n<div class="row">\n  <p><a id="back" href="/"> <-Trang chủ</a></p>\n</div>\n<div class="row">\n  <h2>\n    <span style="color: lightgray"># </span>\n    test\n  </h2>\n</div>\n<br />\n\n<div class="row">\n  <div style="display: flex; flex-direction: column">\n    <small class="post-meta">Ngày: {datetime.today().strftime('%d-%m-%Y')}</small>\n    <small class="post-meta"\n      >Tags: \n      <a href="../tags/test.html" id="tag-name">test</a>\n      \n    </small>\n  </div>\n</div>\n<br />\n\n<p class="post-content"><h1>test header</h1>\n\n<p>test content</p>\n</p>\n \n<script\n  src="https://utteranc.es/client.js"\n  repo="tvph/tvph.github.io"\n  issue-term="url"\n  label="Comment"\n  theme="github-light"\n  crossorigin="anonymous"\n  async\n></script>\n\n      </div>\n    </div>\n    <script src="../static/script.js" type="text/javascript"></script>\n  </body>\n</html>"""

    # print(repr(post_content))
    assert path.joinpath("posts/test.html").exists() == True
    assert test_post_content == post_content


def test_render_tags(test_setup):
    path = test_setup

    _, metadata, tags, info = create_posts(root_path=path.resolve())

    # create tags folder in temp folder
    path.joinpath("tags/").mkdir(mode=511, parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(searchpath="./src/templates"))
    tag_html = env.get_template("tags.html")

    render_tags(
        metadata,
        tags,
        path.joinpath("tags").resolve(),
        tag_html,
        info,
    )

    with open(path.joinpath("tags/test.html"), "r") as f:
        tag_content = f.read()

    test_tag_content = f"""<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <link rel="stylesheet" href="../static/main.css" />\n    <link\n      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"\n      rel="stylesheet"\n      integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU"\n      crossorigin="anonymous"\n    />\n\n    <link\n      rel="stylesheet"\n      href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/base16/solarized-light.min.css"\n      integrity="sha512-ZW2g6Pn2pMbKSyjcA+r4Lc58kcfvOdcsTuCCTl3qz8NqVJwUtAuiN61pDoW3EEfrjwH2CPtkFWMdkzMY1idilA=="\n      crossorigin="anonymous"\n      referrerpolicy="no-referrer"\n    />\n    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>\n    <link\n      rel="stylesheet"\n      href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css"\n      integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p"\n      crossorigin="anonymous"\n    />\n    <link\n      href="https://fonts.googleapis.com/css?family=Inter"\n      rel="stylesheet"\n      crossorigin="anonymous"\n    />\n\n    <title>test blog</title>\n  </head>\n  <body>\n    <div class="main">\n      <div class="heading">\n        <a href="/"\n          ><img\n            id="home-icon"\n            src="my_profile.png"\n            alt="Python Trioxide"\n        /></a>\n        <div class="info">\n          <a href="github.com" title="Github">\n            <i class="fab fa-github-alt"></i\n          ></a>\n          <a href="stackoverflow.com" title="Stack Overflow"\n            ><i class="fab fa-stack-overflow"></i\n          ></a>\n          <a href="linkedin.com" title="LinkedIn"\n            ><i class="fab fa-linkedin"></i\n          ></a>\n          <a href="mailto: email@email.com" title="Email"\n            ><i class="fas fa-at"></i\n          ></a>\n          <a href="resume.pdf" title="Resume"\n            ><i class="fas fa-file"></i\n          ></a>\n        </div>\n      </div>\n      <div id="container">\n        \n<h2>Các bài viết trong tag: <span style="color: lightgreen;">TEST</span></h2>\n<br>\n\n\n  <p>\n  <div class="home-summ">\n    <small class="home-meta">{datetime.today().strftime('%d-%m-%Y')}</small>\n    <br>\n    <small class="home-meta right">tags: \n      \n      <a href="../tags/test.html" id="link-tags">\n        test\n      </a>\n      \n    </small>\n  </div>\n    <h3>\n      <a href="../posts/test.html" id="link-post">\n        test\n      </a>\n    </h3>\n    <small>\n      test\n    </small>\n  </p>\n\n\n \n      </div>\n    </div>\n    <script src="../static/script.js" type="text/javascript"></script>\n  </body>\n</html>"""
    # print(repr(tag_content))
    assert path.joinpath("tags/test.html").exists() == True
    assert test_tag_content == tag_content
