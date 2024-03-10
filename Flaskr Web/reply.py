from flask import(
    Blueprint,g,url_for,redirect,flash,render_template,request
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp=Blueprint('reply',__name__, url_prefix='/blog/reply')

@bp.route('/<int:post_id>/<int:page_number>/')
def index(post_id, page_number=1):
    db=get_db()

    post=db.execute(
        'SELECT p.id, title, body, created, username, p.view_count'
        ' FROM post p JOIN user u ON p.author_id = u.id where p.id = ?',
        (str(post_id),)
    ).fetchall()

    replys=db.execute(
        'SELECT r.id, body, created, parent_id, username, author_id'
        ' from reply r JOIN user u ON r.author_id = u.id where r.parent_id = ?'
        'ORDER BY created DESC'
        ' LIMIT ?,?',
        (str(post_id),(page_number-1)*10, page_number*10)
    ).fetchall()

    row_count = db.execute(
        'SELECT COUNT (parent_id) FROM reply WHERE parent_id=?',(str(post_id),)
    ).fetchall()

    db.execute('update post set view_count=view_count+1 where id=?', (str(post_id),))
    db.commit()

    return render_template('blog/reply/index.html', post=post, replys=replys, page_number=page_number, row_count=row_count)

@bp.route('/<int:post_id>/write', methods=('GET', 'POST'))
@login_required
def write(post_id):
    if request.method == 'POST':
        body = request.form['body']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO reply (body, author_id, parent_id)'
                ' VALUES (?, ?, ?)',
                (body, g.user['id'], post_id)
            )
            db.commit()
            return redirect(url_for('reply.index',post_id=post_id,page_number=1))

    return render_template('blog/reply/write.html', post_id=post_id)

def get_reply(reply_id,view_count,check_author=True):
    reply = get_db().execute(
        'SELECT id, body, created, view_count'
        ' FROM reply where id = ? and view_count=?',
        (str(reply_id),view_count)
    ).fetchone()

    if reply is None:
        abort(404, f"Reply id {id} doesn't exist.")

    return reply

@bp.route('/<post_id>/<int:id>/<int:view_count>/update', methods=('GET', 'POST'))
@login_required
def update(post_id,id,view_count):
    post = get_reply(id,view_count)

    if request.method == 'POST':
        body = request.form['body']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE reply SET body = ?'
                ' WHERE id = ?',
                (body, id)
            )
            db.commit()
            return redirect(url_for('reply.index',post_id=post_id,view_count=view_count,page_number=1))

    return render_template('blog/reply/update.html', reply=post, post_id=post_id)

@bp.route('/<int:id>/<int:view_count>/delete', methods=('POST',))
@login_required
def delete(id,view_count):
    get_reply(id,view_count)
    db = get_db()
    db.execute('DELETE FROM reply WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('blog.index',view_count=view_count))

