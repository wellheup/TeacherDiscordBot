from flask import Flask
from threading import Thread
import os
import psycopg2.pool

pool = psycopg2.pool.SimpleConnectionPool(0,80, os.getenv("DATABASE_URL"))
conn = pool.getconn()
cursor2 = conn.cursor()

app = Flask('')

@app.route('/')
def display_syllabus():
	# cursor2.execute("SELECT * FROM syllabus")
	# rows = cursor2.fetchall()
	# syllabus_str = '<h1>Syllabus Table Contents:</h1>'
	# syllabus_str += '<table style="border-collapse: collapse;">'
	# syllabus_str += '<tr>'
	# for column in cursor2.description:
	# 	syllabus_str += f'<th style="border: 1px solid black;">{column.name}</th>'
	# syllabus_str += '</tr>'
	# for index, row in enumerate(rows):
	# 	syllabus_str += f'<tr style="background-color: {"#f0f0f0" if index % 2 != 0 else "#999999"};">'
	# 	for item in row:
	# 		syllabus_str += f'<td style="border: 1px solid black;">{item}</td>'
	# 	syllabus_str += '</tr>'
	# syllabus_str += '</table>'
	# return syllabus_str
	return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()

