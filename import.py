import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

engine=create_engine(os.getenv("DATABASE_URL"))
db=scoped_session(sessionmaker(bind=engine))
def main():
	with open("books.csv", "r") as file:
		reader=csv.DictReader(file)
		for line in reader:
			author=db.execute("SELECT * FROM authors WHERE name = :name", {"name": line["author"]}).fetchall()
			if len(author)==0:
				db.execute("INSERT INTO authors(name) VALUES (:name)", {"name":line["author"]})
			author=db.execute("SELECT * FROM authors WHERE name=:name", {"name": line["author"]}).fetchall()
			books=db.execute("SELECT * FROM books WHERE name=:name AND author_id=:author_id AND year=:year", {"name": line["title"], "author_id": author[0][0], "year":line["year"]}).fetchall()

			if len(books)==0:
				db.execute("INSERT INTO books(name, author_id, year) VALUES(:name, :author_id, :year)", {"name": line["title"], "author_id": author[0][0], "year": line["year"]})
				db.commit()
			

if __name__=="__main__":
	main()
	db.commit()
