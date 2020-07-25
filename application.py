from flask import Flask, render_template, redirect, request
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pytz import timezone
from datetime import datetime
app=Flask(__name__)
engine=create_engine(os.getenv("DATABASE_URL"))
db=scoped_session(sessionmaker(bind=engine))


@app.route("/")

def index():
	return render_template("index.html")

@app.route("/<string:query>")
def query(query):
	template="<li><h1>Authors</h1></li>"
	authors=db.execute("SELECT * FROM authors WHERE name LIKE :query", {"query": query+"%"}).fetchall()
	books=db.execute("SELECT * FROM books WHERE name LIKE :query", {"query": query+"%"}).fetchall()
	if authors:
		for i in authors:
			template+='<li><a href="/author?q='+str(i[0])+'"'+">"+str(i[1])+"</a></li>"
	template+="<li><h1>Books!</h1></li>"
	if books:
		for i in books:
			template+='<li><a href="/book?q='+str(i[0])+'"'+">"+str(i[1])+", "+str(i[3])+"</a></li>"

	return template
@app.route("/book")
def book():
	id=int(request.args.get("q"))
	book=db.execute("SELECT * FROM books WHERE id=:id", {"id":id}).fetchall()
	author=db.execute("SELECT * FROM authors WHERE id=:author_id", {"author_id": book[0][2]}).fetchall()
	return render_template("book.html", book=book[0], author=author[0])
@app.route("/author")
def author():
	id=request.args.get("q")
	id=int(id)
	author=db.execute("SELECT * FROM authors WHERE id=:id", {"id":id}).fetchall()
	books=db.execute("SELECT * FROM books WHERE author_id=:id", {"id": author[0][0]}).fetchall()
	return render_template("author.html", author=author, books=books)
@app.route("/create_book", methods=["GET", "POST"])
def create_book():
	if request.method=="GET":
		return render_template("add_books.html")
	else:
		name=request.form.get("name")
		author=request.form.get("author")
		year=request.form.get("year")
	
		if not name or not author or not year:
			return render_template("add_books.html")
		try:
			y=int(year)
			if y<0:
				return render_template("add_books.html")
			if y>datetime.now(timezone("US/Eastern")).year:
				return render_template("add_books.html")

		except:
			return render_template("add_books.html")
		author_id=db.execute("SELECT * FROM authors WHERE name=:author", {"author": author}).fetchall()
		if len(author_id)==0:
			return render_template("add_books.html")
		same=db.execute("SELECT * FROM books WHERE name=:name AND author_id=:author_id AND year=:year",{"name":name, "author_id": author_id[0][0], "year":year}).fetchall()
		if len(same)!=0:
			return render_template("add_books.html")
		db.execute("INSERT INTO books(name, author_id, year) VALUES(:name, :author_id, :year)", {"name": name, "author_id": author_id[0][0], "year": year})
		db.commit()
		return redirect("/")

@app.route("/create_author", methods=["GET", "POST"])
def create_author():

	return "author"
