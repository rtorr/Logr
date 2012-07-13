from os import listdir
from os.path import isdir

from flask import Flask, render_template
from flaskext.markdown import Markdown

from utils import slugify

logr = Flask(__name__)
logr.config.from_object('config')
Markdown(logr)

@logr.route('/')
def index():
    """
    Lists all articles, separated by category. This method maps to the front
    page.
    """
    # Create a dictionary `files` that separates articles by category.
    files = dict(Miscellaneous=[])
    for file_ in listdir('articles'):
        if isdir('articles/' + file_):
            files[file_] = []
            for f in listdir('articles/' + file_):
                if f.endswith('.md'):
                    with open('articles/' + file_ + '/' + f, 'r') as f_open:
                        title=f_open.readline()
                        files[file_].append(dict(file_=f, slug=slugify(title), title=title))
        else:
            if file_.endswith('.md'):
                with open('articles/' + file_, 'r') as f_open:
                    title=f_open.readline()
                    files['Miscellaneous'].append(dict(file_=file_, slug=slugify(title), title=title))
    
    return render_template('index.html', files=files)

@logr.route('/b/<slug>', methods=['GET'])
def show(slug):
    """
    Search the database and retrieve the article whose slug matches <slug>.
    Render a template to show this article.
    """
    for dir_ in listdir('articles/'):
        if isdir('articles/' + dir_):
            for file_ in listdir('articles/' + dir_):
                with open('articles/' + dir_ + '/' + file_, 'r') as f_open:
                    if slug == slugify(f_open.readline()):
                        article = 'articles/' + dir_ + '/' + file_
        else:
            with open('articles/' + dir_, 'r') as f_open:
                if slug == slugify(f_open.readline()):
                    article = 'articles/' + dir_

    return render_template('show.html', article=open(article, 'r').read())

if __name__ == '__main__':
    logr.run()
