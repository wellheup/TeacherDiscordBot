from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from utils import daily_update_url, get_current_url
import os
from crud import *
from sqlalchemy.orm import Session
import crud
from replit import db as replit_db


from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import (Column, Integer, String, Text, MetaData, Table, inspect)
from database import SessionLocal, Base
from models import Syllabus
from models import Bugs
from models import Assignments
from models import DemoSyllabus
from models import DemoBugs
from models import DemoAssignments

app = Flask(__name__)
	
current_url_suffix = replit_db.get('url_suffix')
is_live = False if os.getenv('REPLIT_DEPLOYMENT') == '1' else True

@app.route('/', defaults={'url_suffix': ''}, methods=['GET'])
@app.route('/<path:url_suffix>/')
def index(url_suffix):
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	syllabus = get_syllabus(db, is_demo)
	columns = get_columns(db, is_demo)
	pretty_columns = get_pretty_columns(db)
	bugs = get_bugs(db, is_demo)
	assignment = get_current_assignment(db, is_demo)
	graveyard = get_graveyard(db, is_demo)
	todo_unformatted = get_todo(db, is_demo)
	todo = format_todo(todo_unformatted)

	return render_template(
		'index.html', 
		syllabus=syllabus, 
		columns=columns, 
		pretty_columns=pretty_columns, 
		bugs=bugs, 
		assignment=assignment, 
		graveyard=graveyard,
		todo=todo,
		url_suffix="/"+url_suffix+"/" if url_suffix else ""
	)


@app.route('/update', defaults={'url_suffix': ''}, methods=['POST'])
@app.route('/update/<path:url_suffix>/', methods=['POST'])
def update(url_suffix):
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		unique_id = int(request.form.get('unique_id'))
		book = request.form.get('book')
		author = request.form.get('author')
		series = request.form.get('series')
		is_completed = bool(request.form.get('is_completed', False))
		added_by = request.form.get('added_by')
		season = int(request.form.get('season'))
		num_in_series = int(request.form.get('num_in_series'))
		is_extra_credit = bool(request.form.get('is_extra_credit', False))
		date_completed = request.form.get('date_completed')
		up_votes = int(request.form.get('up_votes'))
		down_votes = int(request.form.get('down_votes'))
		genre = request.form.get('genre')

		update_database(
			db, unique_id, book, author, series, is_completed,
			added_by, season, num_in_series, is_extra_credit,
			date_completed, up_votes, down_votes, genre, is_demo
		)
		
		return redirect(url_for(f'index', url_suffix="/"+url_suffix+"/" if url_suffix else ""))

	except Exception as e:
		db.rollback()
		return str(e) + ". Failed to post data.", 500
	finally:
		db.close()


@app.route('/add', defaults={'url_suffix': ''}, methods=['POST'])
@app.route('/add/<path:url_suffix>/', methods=['POST'])
def add(url_suffix):
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		book = request.form.get('book')
		author = request.form.get('author')
		series = request.form.get('series')
		added_by = request.form.get('added_by')
		season = int(request.form.get('season'))
		genre = request.form.get('genre')
		num_in_series = int(request.form.get('num_in_series'))
		is_extra_credit = bool(request.form.get('is_extra_credit', False))

		add_book(db, book, author, series, added_by, season, is_demo, genre, num_in_series, is_extra_credit)

		return redirect(url_for(f'index', url_suffix="/"+url_suffix+"/" if url_suffix else ""))
		
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()

@app.route('/delete', defaults={'url_suffix': ''}, methods=['POST'])
@app.route('/delete/<path:url_suffix>/', methods=['POST'])
def delete(url_suffix):
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		id = int(request.form.get('unique_id'))
		remove_id(db, id, is_demo)
		
		return redirect(url_for(f'index', url_suffix="/"+url_suffix+"/" if url_suffix else ""))
		
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()


@app.route('/complete', defaults={'url_suffix': ''}, methods=['POST'])
@app.route('/complete/<path:url_suffix>/', methods=['POST'])
def complete(url_suffix):
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		book = request.form.get('book')
		complete_book(db, book, is_demo)
		
		return redirect(url_for(f'index', url_suffix="/"+url_suffix+"/" if url_suffix else ""))
		
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()


@app.route('/assign', defaults={'url_suffix': ''}, methods=['POST'])
@app.route('/assign/<path:url_suffix>/', methods=['POST'])
def assign(url_suffix):
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		print("in assign")
		assignment_data = request.form.get('assignment_data')
		add_assignment(db, assignment_data, is_demo)
		
		return redirect(url_for(f'index', url_suffix="/"+url_suffix+"/" if url_suffix else ""))
		
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()
		

@app.route('/report_bug', defaults={'url_suffix': ''}, methods=['POST'])
@app.route('/report_bug/<path:url_suffix>/', methods=['POST'])
def report_bug(url_suffix):
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		description = request.form.get('description')
		print(f"description: {description}")
		added_by = request.form.get('added_by')
		print(f"added_by: {added_by}")
		add_bug(db, description, added_by, is_demo)
		
		return redirect(url_for(f'index', url_suffix="/"+url_suffix+"/" if url_suffix else ""))
		
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()


@app.route('/delete_bug', defaults={'url_suffix': ''}, methods=['POST'])
@app.route('/delete_bug/<path:url_suffix>/', methods=['POST'])
def delete_bug(url_suffix):
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		bug_id = int(request.form.get('bug_id'))
		delete_bug(db, bug_id, is_demo)
		
		return redirect(url_for(f'index', url_suffix="/"+url_suffix+"/" if url_suffix else ""))
		
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()


def format_todo(todo):
	todo_formatted = {}
	for row in todo:
		if row.author in todo_formatted.keys():
			if row.series in todo_formatted[row.author].keys():
				todo_formatted[row.author][row.series].append({'book':row.book, 'id':row.unique_id})
			else:
				todo_formatted[row.author][row.series] =  [{'book':row.book, 'id':row.unique_id}]
		else:
			todo_formatted[row.author] = {row.series: [{'book':row.book, 'id':row.unique_id}]}
	
	return todo_formatted

# TODO: 
# make actual CRUD for all of the tables
# 	Create -post
# 	read - get
# 	update - put
# 	delete - delete