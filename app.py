from flask import Flask, flash, url_for
from flask import render_template, request
import sqlite3 as sql
import os
#from bson.objectid import ObjectId
from werkzeug.exceptions import abort
#if os.path.exists("env.py"):
#    import env


app = Flask(__name__)
#env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
#app.config.from_object(env_config)

def get_db_connection():
    conn = sql.connect('filmflix.db')
    conn.row_factory = sql.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template(
        'index.html', posts = posts
    )
 
@app.route('/insertRecord')
def insertRecord():
   return render_template('insertRecord.html')

@app.route('/updateRecord')
def updateRecord():
   return render_template('updateRecord.html')

@app.route('/deleteRecord')
def deleteRecord():
   return render_template('deleteRecord.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         title = request.form['title']
         yearRld = request.form['yearRld']
         rating = request.form['rating']
         duration = request.form['duration']
         genre = request.form['genre']
         
         with sql.connect("filmflix.db") as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES (?,?,?,?,?)", (title, yearRld, rating, duration, genre))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/updaterec',methods = ['POST', 'GET'])
def updaterec():
   if request.method == 'POST':
      try:
         filmID = request.form['filmID']
         filmID = int(filmID)
         title = request.form['title']
         yearRld = request.form['yearRld']
         yearRld = int(yearRld)
         rating = request.form['rating']
         duration = request.form['duration']
         duration = int(duration)
         genre = request.form['genre']
         
         
         with sql.connect("filmflix.db") as con:
            cur = con.cursor()
            print(cur)
            cur.execute(f"UPDATE tblFilms SET title = ? WHERE filmID = ?", (title, filmID))
            print("execute")
            con.commit()
            msg = "Record successfully updated"
      except:
         con.rollback()
         msg = "error in update operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/deleterec',methods = ['POST', 'GET'])
def deleterec():
   if request.method == 'POST':
      try:
         filmID = request.form['filmID']
         filmID = int(filmID)
         
         with sql.connect("filmflix.db") as con:
            cur = con.cursor()
            print(cur)
            cur.execute(f"DELETE FROM tblFilms WHERE filmID = {filmID}")
            print("execute")
            con.commit()
            msg = "Record successfully deleted"
      except:
         con.rollback()
         msg = "error in delete operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)