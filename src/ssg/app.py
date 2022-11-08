from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template
from markdown2 import markdown
from pathlib import Path
from datetime import datetime
import typing as t
from concurrent.futures import ThreadPoolExecutor
import yaml
import click


# read markdown file then write to a dict
def create_posts(root_path: Path):

    # load yml info
    with open(root_path.joinpath("config.yml"), "r") as f:
        info = yaml.load(f, Loader=yaml.FullLoader)

    posts = {}

    paths = root_path.joinpath("prototypes").resolve()
    for md_post in paths.iterdir():
        with open(md_post.resolve(), "r") as f:
            posts[md_post.name] = markdown(
                f.read(),
                extras=[
                    "metadata",
                    "fenced-code-blocks",
                    "tables",
                    "strike",
                    "task_list",
                    "code-friendly",
                    "numbering",
                    "footnotes",
                ],
            )

    # return a dict with sorted following date created
    posts_for_rendering = {
        p: posts[p]
        for p in sorted(
            posts,
            key=lambda p: datetime.strptime(
                posts[p].metadata["date"], "%d-%m-%Y"
            ),
            reverse=True,
        )
    }

    # get posts_metata - a list from posts dict
    posts_metadata = [
        posts_for_rendering[p].metadata for p in posts_for_rendering
    ]
    # convert tags from string to list in-place in posts_metadata list
    for m in posts_metadata:
        m["tags"] = [element.strip() for element in m["tags"].split(",")]

    # get posts's tags
    tags = [m["tags"] for m in posts_metadata]

    # convert tags from list to set
    tags = set([i for tag in tags for i in tag])

    return posts_for_rendering, posts_metadata, tags, info


# render homepage
def render_home(
    posts_metadata: t.List[dict],
    render_folder: Path,
    tags: t.Set[str],
    template: Template,
    info: dict,
):
    """Render home.html file to root folder."""

    home_html = template.render(posts=posts_metadata, tags=tags, info=info)
    home_path = render_folder.joinpath("index.html").resolve()
    with open(home_path, "w") as f:
        f.write(home_html)


# render posts
def render_posts(
    posts: t.Dict[str, str],
    tags: t.Set[str],
    render_folder: Path,
    template: Template,
    info: dict,
):
    """Render post_metadata['name'].html file to outputs/ folder."""

    for p in posts:
        post_metadata = posts[p].metadata

        post_data = {
            "title": post_metadata["title"],
            "date": post_metadata["date"],
            "tags": post_metadata["tags"],
            "content": posts[p],
        }
        post_html = template.render(post=post_data, tags=tags, info=info)

        # render to html files
        post_path = render_folder.joinpath(
            f"{post_metadata['name']}.html"
        ).resolve()
        with open(post_path, "w") as f:
            f.write(post_html)


def render_tags(
    posts_metadata: t.List[dict],
    tags: t.Set[str],
    render_folder: Path,
    template: Template,
    info: dict,
):

    # build a dict, contains all metadata follow key is tag
    tags_data = {}
    for t in tags:
        tag = []
        for p in posts_metadata:
            if t in p["tags"]:
                tag.append(p)
                tags_data.update({t: tag})

    # print(tags_data)

    # render to html
    for key, value in tags_data.items():
        tag_html = template.render(posts=value, tag=key, info=info)

        tag_path = render_folder.joinpath(f"{key.lower()}.html").resolve()
        with open(tag_path, "w") as f:
            f.write(tag_html)


@click.command()
def run():
    root = Path(__file__).parent.parent.parent.resolve()
    posts, metadata, tags, info = create_posts(root)

    env = Environment(
        loader=FileSystemLoader(
            searchpath=root.joinpath("src/").joinpath("templates/")
        )
    )
    home_template = env.get_template(name="home.html")
    post_template = env.get_template(name="post.html")
    tag_template = env.get_template(name="tags.html")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(
            render_home,
            metadata,
            root,
            tags,
            home_template,
            info,
        )
        executor.submit(
            render_posts,
            posts,
            tags,
            root.joinpath("posts").resolve(),
            post_template,
            info,
        )
        executor.submit(
            render_tags,
            metadata,
            tags,
            root.joinpath("tags").resolve(),
            tag_template,
            info,
        )
