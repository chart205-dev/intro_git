from flask_1030 import app
from flask import render_template, redirect, url_for, request
import sqlite3 

DATABASE = 'database.db'

@app.route('/')
def index():
 con = sqlite3.connect(DATABASE)
 db_books = con.execute("SELECT * FROM books").fetchall()
 books = []
 
 for book in db_books:
  books.append({
   'title': book[0],
   'price': book[1],
   'arrival_day': book[2]
})
 return render_template(
  'index.html',
  books=books
 )

@app.route('/form')
def form():
 return render_template('form.html')

@app.route('/register', methods=['POST'])
def register():
 title = request.form['title'] 
 price = request.form['price']
 arrival_day = request.form['arrival_day']

 con = sqlite3.connect(DATABASE)
 con.execute(
  "INSERT INTO books VALUES (?, ?, ?)",
  [title, price, arrival_day]
 )
 con.commit()
 con.close()

 return redirect(url_for('index'))