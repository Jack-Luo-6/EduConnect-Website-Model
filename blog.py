from flask import(
    Blueprint,g,url_for,redirect,flash,render_template,request
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp=Blueprint('blog',__name__)

@bp.route('/')
@bp.route('/<int:page_number>/')
def index(page_number=1):
    db=get_db()
    posts=db.execute(
        'SELECT p.id, title, body, created, author_id, username, view_count'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY view_count DESC'
        ' LIMIT ?,?',
        ((page_number-1)*10, page_number*10)
    ).fetchall()

    row_count=db.execute(
        'SELECT COUNT(*) FROM post'
    ).fetchall()

    return render_template('blog/index.html',posts=posts,page_number=page_number, row_count=row_count)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id,view_count,check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, p.view_count'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ? and p.view_count = ?',
        (id,view_count)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403, f"Post id doesn't match")

    return post

@bp.route('/<int:id>/<int:view_count>/update', methods=('GET', 'POST'))
@login_required
def update(id, view_count):
    post = get_post(id, view_count)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post,view_count=view_count)

@bp.route('/<int:id>/<int:view_count>/delete', methods=('POST',))
@login_required
def delete(id,view_count):
    get_post(id,view_count)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('blog.index',view_count=view_count))

