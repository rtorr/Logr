from os import listdir
from os.path import isdir, isfile

from flask import Flask, render_template
from flaskext.markdown import Markdown

from utils import slugify

logr = Flask(__name__)
logr.config.from_object('config')
Markdown(logr)

ARTICLE_DIR = logr.config['ARTICLE_DIR']

@logr.route('/')
def index():
    """
    Lists all articles, separated by category. This method maps to the front
    page.
    """
    # Create a dictionary `files` that separates articles by category.
    for file_ in listdir(ARTICLE_DIR):
        if isfile(ARTICLE_DIR + file_) and file_ != 'empty':
            files = dict(Miscellaneous=[])
            break
        files = dict()

    for file_ in listdir(ARTICLE_DIR):
        if isdir(ARTICLE_DIR + file_):
            files[file_] = []
            for f in listdir(ARTICLE_DIR + file_):
                if f.endswith('.md'):
                    with open(ARTICLE_DIR + file_ + '/' + f, 'r') as f_open:
                        title=f_open.readline()
                        files[file_].append(dict(file_=f, slug=slugify(title), title=title.decode('utf-8')))
        else:
            if file_.endswith('.md'):
                with open(ARTICLE_DIR + file_, 'r') as f_open:
                    title=f_open.readline()
                    files['Miscellaneous'].append(dict(file_=file_, slug=slugify(title), title=title))

    blurb = open('pages/front.md', 'r').read()

    return render_template('index.html', files=files, blurb=blurb)

@logr.route('/b/<slug>', methods=['GET'])
def show(slug):
    """
    Search the database and retrieve the article whose slug matches <slug>.
    Render a template to show this article.
    """
    for dir_ in listdir(ARTICLE_DIR):
        if isdir(ARTICLE_DIR + dir_):
            for file_ in listdir(ARTICLE_DIR + dir_):
                with open(ARTICLE_DIR + dir_ + '/' + file_, 'r') as f_open:
                    if slug == slugify(f_open.readline()):
                        article = ARTICLE_DIR + dir_ + '/' + file_
        else:
            with open(ARTICLE_DIR + dir_, 'r') as f_open:
                if slug == slugify(f_open.readline()):
                    article = ARTICLE_DIR + dir_

    title = open(article, 'r').readline().decode('utf8')
    source = open(article, 'r').read().decode('utf8')

    return render_template('show.html', article=dict(title=title, source=source))

if __name__ == '__main__':
    logr.run()
