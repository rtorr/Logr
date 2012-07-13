from os import listdir
from os.path import isdir

from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
from flaskext.markdown import Markdown

from utils import establish_db_connection, slugify

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
    print files
    return render_template('index.html', files=files)

@logr.route('/new', methods=['POST', 'GET'])
def new():
    """
    Display the 'new post' form. If request type is POST, form has been
    submitted and will be processed.
    """
    # If there is no session, the user does not belong here.
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':
        article_info = [request.form['post-title'], 
                        request.form['post-body'],
                        request.form['post-cat'],
                        slugify(request.form['post-title'])]
                        
        g.db.execute('INSERT INTO articles (title, body, cat, slug) values \
                     (?, ?, ?, ?)', article_info)
        g.db.commit()
        flash('"%s" was successfully posted.' % (request.form['post-title'],))
        return redirect(url_for('index'))
    
    categories = g.db.execute('SELECT name FROM categories ORDER BY name DESC')
    categories = categories.fetchall()
    return render_template('new.html', categories=categories)

@logr.route('/cat', methods=['POST', 'GET'])
def cat():
    """
    Display the 'new category' form. If request type is POST, form has been 
    submitted and will be processed.
    """
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':
        g.db.execute('INSERT INTO categories (name) values (?)',
                     [request.form['cat-name']])
        g.db.commit()
        flash('Category "%s" has been added to the database.' %
                (request.form['cat-name']))
        return redirect(url_for('index'))
    return render_template('cat.html')

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

@logr.route('/login', methods=['POST', 'GET'])
def login():
    """
    Display the login form for the user. If the request type is 'POST' then we
    validate the user's username and password combination. If they are correct,
    then create a session and redirect them to the front page. Otherwise,
    display and error.
    """
    error = None
    if request.method == 'POST':
        if request.form['username'] != logr.config['USERNAME']:
            error = 'Invalid username.'
        elif request.form['password'] != logr.config['PASSWORD']:
            error = 'Invalid password.'
        else:
            session['logged_in'] = True
            flash('Welcome back!')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@logr.route('/logout')
def logout():
    """
    Log the user out.
    """
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(url_for('index'))

@logr.before_request
def before_request():
    """
    A special function that get's called before each request and establishes a
    connection to the database.
    """
    g.db = establish_db_connection(logr.config['DATABASE_FILE'])

@logr.teardown_request
def teardown_request(exception):
    """
    A special function that gets called after the response has been constructed
    and closes the database connection opened by before_request().
    """
    g.db.close()


if __name__ == '__main__':
    logr.run()
