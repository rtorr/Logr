from flask import Flask, request, session, g, redirect, url_for, abort, \
         render_template, flash
from utils import establish_db_connection, slugify


# Initiate Flask and load config settings from config.py
bh = Flask(__name__)
bh.config.from_object('config')


"""
The entry point to BrewerHimself.com.

@return -- Renders index.html.
"""
@bh.route('/')
def index():
    categories = g.db.execute('SELECT name FROM categories ORDER BY name DESC').fetchall()
    article_dict = []
    for category in categories:
        name = category
        articles = g.db.execute('SELECT title, body, slug FROM articles WHERE cat=? ORDER BY id DESC', [name[0]])
        articles = [dict(title=row[0], body=row[1], slug=row[2]) for row in articles.fetchall()]
        article_dict.append(dict(name=category, articles=articles))

    c = g.db.execute('SELECT title, body, slug FROM articles ORDER BY id DESC')
    articles = [dict(title=row[0], body=row[1], slug=row[2]) for row in c.fetchall()]
    return render_template('index.html', articles=articles, article_dict=article_dict, categories=categories)


"""
First, we check whether the user is logged in. If not, immediately abort
because they don't belong here. Second, check headers to see if this is
a POST request. If so, enter the new article into the database and redirect
to /. Otherwise, render new.html.

@return -- Redirect to / if request.method == POST, otherwise render new.html.
"""
@bh.route('/new', methods=['POST', 'GET'])
def new():
    if not session.get('logged_in'): abort(401)
    if request.method == 'POST':
        g.db.execute('INSERT INTO articles (title, body, slug, cat) values (?, ?, ?, ?)', 
                [request.form['post-title'], 
                 request.form['post-body'], 
                 slugify(request.form['post-title']),
                 request.form['post-cat']])
        g.db.commit()

        flash('"%s" was successfully posted.' % (request.form['post-title'],))
        return redirect(url_for('index'))

    categories = g.db.execute('SELECT name FROM categories ORDER BY name DESC').fetchall()
    return render_template('new.html', categories=categories)


@bh.route('/cat', methods=['POST', 'GET'])
def cat():
    if not session.get('logged_in'): abort(401)
    if request.method == 'POST':
        g.db.execute('INSERT INTO categories (name) values (?)',
                [request.form['cat-name']])
        g.db.commit()

        flash('Category "%s" has been added to the database.' % (request.form['cat-name']))
        return redirect(url_for('index'))
    return render_template('cat.html')


@bh.route('/b/<slug>', methods=['GET'])
def show(slug):
    c = g.db.execute('SELECT title, body, slug, cat FROM articles WHERE slug=?', (slug,)).fetchone()
    print c
    article = dict(title=c[0], body=c[1], slug=c[2], cat=c[3])
    return render_template('show.html', article=article)


"""
Validates the user's username and password combinator and, if it is legit,
logs them in and returns them to the front page. If an error occurs, the user
is informed and asked for their information again.

@return -- Redirect to / if username and password match the set stored in the
           configuration. If request.method != 'POST', render login.html.
"""
@bh.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != bh.config['USERNAME']:
            error = 'Invalid username.'
        elif request.form['password'] != bh.config['PASSWORD']:
            error = 'Invalid password.'
        else:
            session['logged_in'] = True
            flash('Welcome back!')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


"""
Log the user out. By using session's pop() method with a second paramether None,
'logged_in' will be deleted if it's present, otherwise nothing will happen. This
way, we don't even have to check if the user is logged in.
"""
@bh.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(url_for('index'))

"""
A special function that get's called before each request and establishes a
connection to the database.
"""
@bh.before_request
def before_request():
    g.db = establish_db_connection(bh.config['DATABASE'])


"""
A special function that get's called after the response has been constructed
and closes the database connection opened by before_request().
"""
@bh.teardown_request
def teardown_request(exception):
    g.db.close()


if __name__ == '__main__':
    bh.run()
