from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
db_location = 'var/data.db'

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def dis_home():
    return render_template('home.html')


@app.route('/search/', methods=['POST','GET'])
def dis_search():
    db = get_db()
    if request.method == 'POST':
        print (request.form)
        term = request.form['search']
        sql2 = "SELECT * FROM albums WHERE artist LIKE '%" + term + "%' OR title LIKE '%" + term + "%' OR year_of_release LIKE '%" + term + "%' OR genre LIKE '%" + term + "%'"
        return render_template('results.html', results=db.cursor().execute(sql2))
    else:
        return render_template('search.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

