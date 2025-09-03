from flask import Flask, render_template, request 
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "marine.db"

def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

@app.route('/')
def render_home():
    return render_template('index.html')

@app.route('/main/<fish>')
def render_animals(fish):
    title = fish.upper()
    query = "SELECT animal_name, science_name FROM Marine"
    con = create_connection(DATABASE)
    cur = con.cursor()
    #query the database 
    cur.execute(query)
    animal_list = cur.fetchall()
    con.close()
    print(animal_list)
    return render_template('creatures.html', animals=animal_list, title=title)

@app.route("/search", methods=['GET','POST'])
def render_search():
    search = request.form['search']
    title = "Search for " + search
    query = "SELECT animal_name, science_name, image FROM Marine WHERE animal_group = ?"
    search = "%" +search+ "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search))
    animal_list = cur.fetchall()
    con.close()
    return render_template('cretures.html', animals=animal_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

