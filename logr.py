from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash

from utils import establish_db_connection, slugify

logr = Flask(__name__)
logr.config.from_object('config')


@logr.route('/')
def index():
    """
    Maps to the / directory and lists articles, separated by category.
    """
    article_dict = []
    categories = g.db.execute('SELECT name FROM categories ORDER BY name DESC')
    categories = categories.fetchall()
    for category in categories:
        articles = g.db.execute('SELECT title, body, slug FROM articles WHERE \
                                cat=? ORDER BY id DESC', [category[0]])
        articles = articles.fetchall()
        # Turn articles into a list of dicts to make the template more readable
        articles = [dict(title=row[0], 
                         body=row[1], 
                         slug=row[2]) for row in articles]
        article_dict.append(dict(category=category, articles=articles))        
    
    return render_template('index.html', article_dict=article_dict, 
                           categories=categories)

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
    article = g.db.execute('SELECT title, body, slug, cat FROM articles \
                            WHERE slug=?', (slug,)).fetchone()
    article = dict(title=article[0], body=article[1], slug=article[2], 
                   category=article[3])
    return render_template('show.html', article=article)

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
