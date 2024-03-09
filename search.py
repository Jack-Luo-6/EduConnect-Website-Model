from flask import(
    Blueprint,flash,render_template,request
)
from flaskr.db import get_db

bp=Blueprint('search',__name__)

@bp.route('/search/',methods=('GET','POST'))
@bp.route('/search/<string:searchword>/<int:page_number>/',methods=('GET','POST'))
def index(searchword='',page_number=1):
    if request.method == 'POST' or len(searchword)>0:
        if request.method == 'POST':
            searchword = request.form['searchword']+'%'
        db = get_db()
        try:
            posts = db.execute(
                "SELECT * FROM post WHERE body LIKE ? LIMIT ?,?", (searchword,(page_number-1)*10, page_number*10)
            ).fetchall()

            row_count = db.execute(
                'SELECT COUNT(*) FROM post'
            ).fetchall()
        except db.IntegrityError:
            error=f"no results found"
        else:
            return render_template('search/results.html', posts=posts, page_number=page_number, row_count=row_count,searchword=searchword)

        flash(error)

    return render_template('search/index.html')

