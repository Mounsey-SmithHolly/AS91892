from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "Marine.db"

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

@app.route('/animals')
def render_animals():
    query = "SELECT animal_name, science_name FROM marine"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()
    #query the database 
    cur.execute(query)
    animal_list = cur.fetchall()
    con.close()
    print(animal_list)
    return render_template('animals.html')




if __name__ == "__main__":
    app.run(host='0.0.0.0')

