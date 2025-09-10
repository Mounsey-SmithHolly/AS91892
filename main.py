from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

# in terminal write python main.py

app = Flask(__name__)
DATABASE = "marine.db"

def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

def get_animals(animal_type):
    title = animal_type.capitalize()
    query = "SELECT animal_name, science_name, life_span, average_length, top_speed, images FROM Marine WHERE animal_group = ?"
    params = [title]
    
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, params)
    animal_list = cur.fetchall()
    print(animal_list)
    con.close()
    return animal_list

def get_classifications():
    con = create_connection(DATABASE)
    query = "SELECT DISTINCT animal_group FROM Marine ORDER BY animal_group ASC"
    cur = con.cursor()
    cur.execute(query)
    records = cur.fetchall()
    for i in range(len(records)):
        records[i] = records[i][0]
    return records

@app.route('/')
def render_home():
    return render_template('index.html', classifications=get_classifications())

@app.route('/main/<classification>')
def render_animals(classification):
    title = classification.upper()
    return render_template('creatures.html', animals=get_animals(classification), title=title, classifications=get_classifications())

#adding in the search function 
@app.route("/search", methods=['GET','POST'])
def render_search():
    search = request.form['search']
    title = "Search for " + search
    query = "SELECT animal_name, science_name FROM Marine WHERE animal_name LIKE ? OR science_name LIKE ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search))
    animal_list = cur.fetchall()
    con.close()
    return render_template('creatures.html', animals=animal_list, title=title, classifications=get_classifications())

@app.route('/sort/<title>')
def render_sortpage(title):
    sort = request.args.get('sort')
    order = request.args.get('order', 'asc')
    #change the sort order 
    if order == 'asc':
        new_order = 'desc'
    else:
        new_order = 'asc'

    #sorting query
    query = "SELECT animal_name, science_name, life_span, average_length, top_speed, images FROM Marine WHERE animal_group=? ORDER BY " + sort+ " " + order
    con = create_connection(DATABASE)
    cur = con.cursor()

    #query the database
    cur.execute(query, (title,))
    animal_list = cur.fetchall()
    con.close()
    return render_template('creatures.html', animals=animal_list, title=title, classifications=get_classifications(), order=new_order)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)