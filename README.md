# This is a small tool to render personal blog

![Blog generator tool](https://github.com/tvph/ssg/actions/workflows/python-app.yml/badge.svg)

## Prerequisite

1. `make`
2. `python`
3. `poetry`

## Usage

* I've created a [tool](https://github.com/tvph/ssg) to render from markdown file to static site by `Python` for my self.
* To use this template, you need to clone the repo first. The project should have this structure:

```
    |_ prototypes/       # contains .md file, you will write your posts in here.
    |_ posts/            # contains all html posts file after run ./render
    |_ tags/             # contains all html tags file after run ./render
    |_ templates/        # contains jinja templates for constructing posts, tags html files
    |_ static/           # contains static file like styles or script for your pages
    |_ index.html        # home page of blog
    |_ app.py            # blog generator tool
    |_ test_app.py       # test all functions of blog generator tool
    |_ Makefile          # command for render html files
    |_ requirements.txt  # for create environment for github actions
    |_ poetry.lock
    |_ pyproject.toml

```

* Firstly, if this is the first time you use this tool:
    * You need to `fork` this repo to your, then change the name of repo following this format: `<your_github_username>.github.io`. And cloning it to your local machine: `git clone https://github.com/...`.
    * Then you need to create `prototypes`, `tags` and `posts` folder by run: `make init`.

* Secondly, you need to install environment to render blog. Run: `make install`.

* Then go to `prototypes` folder and write the your posts in `.md` format, edit the metadata and push them into `prototypes` folder. Notice that, the metadata of .md file you need to keep following these formats

```
title: ....
date: ....
tags: ....
name: ....
summary: ....
```
* After the first time, you only need to write posts and render to html.

* To render blog posts:

	* Run `make clean` to delete old html files.
	* Run `make test` to run test.
	* Run `make run` to render all html files to `posts` and `tags` folder.

* Push to your repo, and go to `https://<your_github_username>.github.io/` to see.

* To read more about `github pages`. Read [this guide](https://pages.github.com/)

* In addition, you can add a comment plugin your self call [utterances](https://utteranc.es/?installation_id=19767855&setup_action=install). After that, go to
`templates/post.html` and replace the script in `{% block script %}{% endblock %}` with your script.

* You can put your information into `config.yml` file

@LICENSE: [MIT](https://github.com/tvph/ssg/blob/master/LICENSE)
