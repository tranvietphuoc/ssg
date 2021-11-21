import pytest
from app import create_posts, render_home, render_posts, render_tags
from jinja2 import Environment, FileSystemLoader
import pathlib
from datetime import datetime
import tempfile
import shutil


@pytest.fixture
def test_setup():

    # write md contents

    path = tempfile.mkdtemp()
    prototypes_path = pathlib.Path(path).joinpath("prototypes").resolve()
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

    yield test_md

    # tear down
    shutil.rmtree(test_md.parent.parent.resolve())  # rm all files in mkdtemp


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

    posts, metadata, tags = create_posts(path.parent.parent.resolve())

    assert posts == test_post
    assert metadata == test_metadata
    assert tags == test_tags


def test_render_home(test_setup):
    path = test_setup

    # mk tests folder

    _, metadata, tags = create_posts(path.parent.parent.resolve())
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    home_template = env.get_template("home.html")

    render_home(metadata, path.parent.parent.resolve(), tags, home_template)

    # test_index_content
    with open(path.parent.parent.joinpath("index.html"), "r") as f:
        index_content = f.read()

    test_index_content = f"""<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <link rel="stylesheet" href="../static/main.css" />\n    <link\n      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"\n      rel="stylesheet"\n      integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU"\n      crossorigin="anonymous"\n    />\n    <link\n      rel="stylesheet"\n      href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css"\n    />\n\n    <link\n      rel="stylesheet"\n      type="text/css"\n      href="//fonts.googleapis.com/css?family=Droid+Sans+Mono"\n    />\n    <title>Phuoc\'s blog</title>\n  </head>\n  <body>\n    <br />\n    <div class="container">\n      <div class="row">\n        <div class="col-sm-2">\n          <h1 class="home-page">\n            <a\n              style="text-decoration: none; color: orangered;"\n              href="../index.html"\n              >Trang chủ</a\n            >\n          </h1>\n        </div>\n        <div class="col-sm-10">\n          \n<h1>Tất cả các bài viết</h1><br>\n\n\n  <p>\n  <div class="home-summ">\n    <small class="home-meta">{datetime.today().strftime('%d-%m-%Y')}</small>\n    <br>\n    <small class="home-meta right">\n      tags: \n       \n        <a href="tags/test.html" style="text-decoration: none; color: orchid;">test</a>\n      \n    </small>\n  </div>\n    <h2>\n      <a href="../posts/test.html" style="text-decoration: none; color: orangered">\n        test\n      </a>\n    </h2>\n    <small>\n      test\n    </small>\n  </p>\n\n\n        </div>\n      </div>\n    </div>\n    <br />\n    <div class="footer">\n      <div class="container">\n        <div class="row">\n          <div class="col-sm-4"></div>\n          <div class="col-sm-4 author">\n            <span class="text-muted"\n              >Powered by\n              <a\n                style="text-decoration: none; color: orangered;"\n                href="https://github.com/tvph"\n                >Trần Việt Phước</a\n              >\n            </span>\n          </div>\n          <div class="col-sm-4"></div>\n        </div>\n      </div>\n    </div>\n    \n    <script src="../static/script.js" type="text/javascript"></script>\n    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>\n  </body>\n</html>"""
    # check file index.html is exists
    # print(repr(index_content))
    assert path.parent.parent.joinpath("index.html").exists() == True
    assert test_index_content == index_content


def test_render_posts(test_setup):
    path = test_setup

    # create posts folder in temp folder
    path.parent.parent.joinpath("posts").mkdir(
        mode=511, parents=True, exist_ok=True
    )

    posts, _, tags = create_posts(root_path=path.parent.parent.resolve())
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    post_html = env.get_template("post.html")

    render_posts(
        posts, tags, path.parent.parent.joinpath("posts").resolve(), post_html
    )

    with open(path.parent.parent.joinpath("posts/test.html"), "r") as f:
        post_content = f.read()

    test_post_content = f"""<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <link rel="stylesheet" href="../static/main.css" />\n    <link\n      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"\n      rel="stylesheet"\n      integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU"\n      crossorigin="anonymous"\n    />\n    <link\n      rel="stylesheet"\n      href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css"\n    />\n\n    <link\n      rel="stylesheet"\n      type="text/css"\n      href="//fonts.googleapis.com/css?family=Droid+Sans+Mono"\n    />\n    <title>Phuoc\'s blog</title>\n  </head>\n  <body>\n    <br />\n    <div class="container">\n      <div class="row">\n        <div class="col-sm-2">\n          <h1 class="home-page">\n            <a\n              style="text-decoration: none; color: orangered;"\n              href="../index.html"\n              >Trang chủ</a\n            >\n          </h1>\n        </div>\n        <div class="col-sm-10">\n          \n<div class="row">\n  <h1>\n    <span style="color: lightgrey;"># </span>\n    test\n  </h1>\n</div>\n<br />\n\n<div class="row">\n  <div style="display: flex; flex-direction: column;">\n    <small class="post-meta">Ngày: {datetime.today().strftime('%d-%m-%Y')}</small>\n    <small class="post-meta"\n      >Tags: \n      <a\n        href="../tags/test.html"\n        style="\n          text-decoration: none;\n          color: orangered;\n          background-color: lightgray;\n        "\n        >test</a\n      >\n      \n    </small>\n  </div>\n</div>\n<br />\n\n<p class="post-content">\n  <h1>test header</h1>\n\n<p>test content</p>\n\n</p>\n\n\n        </div>\n      </div>\n    </div>\n    <br />\n    <div class="footer">\n      <div class="container">\n        <div class="row">\n          <div class="col-sm-4"></div>\n          <div class="col-sm-4 author">\n            <span class="text-muted"\n              >Powered by\n              <a\n                style="text-decoration: none; color: orangered;"\n                href="https://github.com/tvph"\n                >Trần Việt Phước</a\n              >\n            </span>\n          </div>\n          <div class="col-sm-4"></div>\n        </div>\n      </div>\n    </div>\n    \n<script\n  src="https://utteranc.es/client.js"\n  repo="tvph/tvph.github.io"\n  issue-term="url"\n  label="Comment"\n  theme="github-light"\n  crossorigin="anonymous"\n  async\n></script>\n\n    <script src="../static/script.js" type="text/javascript"></script>\n    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>\n  </body>\n</html>"""

    # print(repr(post_content))
    assert path.parent.parent.joinpath("posts/test.html").exists() == True
    assert test_post_content == post_content


def test_render_tags(test_setup):
    path = test_setup

    _, metadata, tags = create_posts(root_path=path.parent.parent.resolve())

    # create tags folder in temp folder
    path.parent.parent.joinpath("tags").mkdir(
        mode=511, parents=True, exist_ok=True
    )
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    tag_html = env.get_template("tags.html")

    render_tags(
        metadata, tags, path.parent.parent.joinpath("tags").resolve(), tag_html
    )

    with open(path.parent.parent.joinpath("tags/test.html"), "r") as f:
        tag_content = f.read()

    test_tag_content = f"""<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <link rel="stylesheet" href="../static/main.css" />\n    <link\n      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"\n      rel="stylesheet"\n      integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU"\n      crossorigin="anonymous"\n    />\n    <link\n      rel="stylesheet"\n      href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css"\n    />\n\n    <link\n      rel="stylesheet"\n      type="text/css"\n      href="//fonts.googleapis.com/css?family=Droid+Sans+Mono"\n    />\n    <title>Phuoc\'s blog</title>\n  </head>\n  <body>\n    <br />\n    <div class="container">\n      <div class="row">\n        <div class="col-sm-2">\n          <h1 class="home-page">\n            <a\n              style="text-decoration: none; color: orangered;"\n              href="../index.html"\n              >Trang chủ</a\n            >\n          </h1>\n        </div>\n        <div class="col-sm-10">\n          \n<h1>Các bài viết trong tag: <span style="color: lightgray;">TEST</span></h1>\n<br>\n\n\n  <p>\n  <div class="home-summ">\n    <small class="home-meta">{datetime.today().strftime('%d-%m-%Y')}</small>\n    <br>\n    <small class="home-meta right">tags: \n      \n      <a href="../tags/test.html" style="text-decoration: none; color: orchid;">\n        test\n      </a>\n      \n    </small>\n  </div>\n    <h3>\n      <a href="../posts/test.html" style="text-decoration: none; color: orangered">\n        test\n      </a>\n    </h3>\n    <small>\n      test\n    </small>\n  </p>\n\n\n\n        </div>\n      </div>\n    </div>\n    <br />\n    <div class="footer">\n      <div class="container">\n        <div class="row">\n          <div class="col-sm-4"></div>\n          <div class="col-sm-4 author">\n            <span class="text-muted"\n              >Powered by\n              <a\n                style="text-decoration: none; color: orangered;"\n                href="https://github.com/tvph"\n                >Trần Việt Phước</a\n              >\n            </span>\n          </div>\n          <div class="col-sm-4"></div>\n        </div>\n      </div>\n    </div>\n    \n    <script src="../static/script.js" type="text/javascript"></script>\n    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>\n  </body>\n</html>"""
    # print(repr(tag_content))

    assert path.parent.parent.joinpath("tags/test.html").exists() == True
    assert test_tag_content == tag_content
