import sqlite3

con = sqlite3.connect("society.db")

c = con.cursor()

#c.execute("create table student(id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, email TEXT, password TEXT)")

c.execute("CREATE TABLE   IF NOT EXISTS  flats ( id INTEGER PRIMARY KEY AUTOINCREMENT, flat_no TEXT,owner_name TEXT, contact TEXT, alt_contact TEXT)")
c.execute("CREATE TABLE  IF NOT EXISTS  maintenance (id INTEGER PRIMARY KEY AUTOINCREMENT, flat_no TEXT NOT NULL , month TEXT NOT NULL,amount INTEGER NOT NULL)")

con.commit()
con.close()
