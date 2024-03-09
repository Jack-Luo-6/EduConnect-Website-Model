from flask import(
    Blueprint,url_for,redirect,flash,render_template,request,session,g
)
from flaskr.auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp=Blueprint('personal_information',__name__)

@bp.route('/personal')
@bp.route('/personal/<int:page_number>/')
def index(page_number=1):
    db=get_db()
    personalinfo=db.execute(
        'SELECT username, id FROM user where id='+str(session['user_id'])
    ).fetchall()

    post=db.execute(
        'SELECT title, body, created, view_count, author_id, id FROM post where author_id=?'
        'LIMIT ?,?',
        (str(session['user_id']),(page_number - 1) * 10, page_number * 10)
    ).fetchall()

    row_count = db.execute(
        'SELECT COUNT(author_id) FROM post WHERE author_id=?'
        ,(str(session['user_id']))
    ).fetchall()

    return render_template('personal_information/index.html',personalinfo=personalinfo,post=post,page_number=page_number,row_count=row_count)

def get_info(id):
    post = get_db().execute(
        'SELECT username, password FROM user where id='+str(id)
    ).fetchone()

    return post

@bp.route('/personal/update', methods=('GET', 'POST'))
@login_required
def update():
    post = get_info(session['user_id'])

    if request.method == 'POST':
        username = request.form['username']
        error = None

        if not username:
            error = 'Username is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'update user set username= ? where id= ?',
                (username,session['user_id'])
            )
            db.commit()
            return redirect(url_for('personal_information.index'))

    return render_template('personal_information/update.html', post=post)

@bp.route('/personal/password', methods=('GET', 'POST'))
@login_required
def password():

    post = get_info(session['user_id'])

    if request.method == 'POST':
        password = request.form['password']
        error = None

        if not password:
            error = 'Password is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            user=db.execute(
                'SELECT password FROM user WHERE id= ?',
                (session['user_id'],)
            ).fetchone()

        if not check_password_hash(user['password'], (password)):
            error = 'Incorrect Password'

        if error is not None:
            flash(error)

        if error is None:
            return redirect(url_for('personal_information.change'))

    return render_template('personal_information/password.html', post=post)

@bp.route('/personal/change', methods=('GET', 'POST'))
@login_required
def change():
    if request.method=='POST':
        password=request.form['password']
        db=get_db()
        error=None

        if not password:
            error='Password is required'

        if error is None:
            db.execute(
                'update user set password= ? where id= ?',
                (generate_password_hash(password),session['user_id'])
            )
            db.commit()
            return redirect(url_for('personal_information.index'))

    return render_template('personal_information/change.html')