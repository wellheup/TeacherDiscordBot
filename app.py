from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from replit import db as replit_db
import os
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from crud import *
from database import SessionLocal, Base
from utils import daily_update_url, get_current_url
from models import Syllabus, Bugs, Assignments, DemoSyllabus, DemoBugs, DemoAssignments

app = Flask(__name__)
bootstrap = Bootstrap(app)

current_url_suffix = replit_db.get('url_suffix')
# is_live = False if os.getenv('REPLIT_DEPLOYMENT') == '1' else True # for replit deployment later

@app.route('/', methods=['GET'])
def index():
	url_suffix = request.args.get('url_suffix', '')
	is_demo = not url_suffix or url_suffix != current_url_suffix
	return render_template('index.html', is_demo=is_demo)


@app.route('/syllabus', methods=['GET'])
def syllabus_content():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = not url_suffix or url_suffix != current_url_suffix
	try:
		syllabus = get_syllabus(db, is_demo)
		columns = get_columns(db, is_demo)
		pretty_columns = get_pretty_columns(db)
		assignment = get_current_assignment(db, is_demo)
		return render_template('syllabus.html',
			syllabus=syllabus, 
			columns=columns, 
			pretty_columns=pretty_columns,
			assignment=assignment,
			demo="DEMO " if is_demo else "",
			url_suffix=url_suffix
		)
	except Exception as e:
		db.rollback()
		return f"{e}. Failed to get syllabus data.", 500
	finally:
		db.close()


@app.route('/update', methods=['POST'])
def update():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = not url_suffix or url_suffix != current_url_suffix
	try:
		data = {
			'book': request.form.get('book'),
			'author': request.form.get('author'),
			'series': request.form.get('series'),
			'is_completed': bool(request.form.get('is_completed', False)),
			'added_by': request.form.get('added_by'),
			'season': int(request.form.get('season')),
			'num_in_series': int(request.form.get('num_in_series')),
			'is_extra_credit': bool(request.form.get('is_extra_credit', False)),
			'date_completed': request.form.get('date_completed'),
			'up_votes': int(request.form.get('up_votes')),
			'down_votes': int(request.form.get('down_votes')),
			'genre': request.form.get('genre'),
			'unique_id': int(request.form.get('unique_id'))
		}
		update_database(db, **data, is_demo=is_demo)
		return renderSyllabus(db, is_demo, url_suffix)
	except Exception as e:
		db.rollback()
		return str(e) + ". Failed to post data.", 500
	finally:
		db.close()


@app.route('/add', methods=['POST'])
def add():
	url_suffix = request.args.get('url_suffix', '')
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
		return renderSyllabus(db, is_demo, url_suffix)
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()
		

@app.route('/delete', methods=['POST'])
def delete():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		id = int(request.form.get('unique_id'))
		remove_id(db, id, is_demo)
		return renderSyllabus(db, is_demo, url_suffix)
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()


@app.route('/complete', methods=['POST'])
def complete():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		book = request.form.get('book')
		complete_book(db, book, is_demo)
		return renderSyllabus(db, is_demo, url_suffix)
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()


@app.route('/assign', methods=['POST'])
def assign():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		assignment_data = request.form.get('assignment_data')
		add_assignment(db, assignment_data, is_demo)
		return renderSyllabus(db, is_demo, url_suffix)
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()


@app.route('/graveyard', methods=['GET'])
def graveyard_content():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		graveyard = get_graveyard(db, is_demo)
		return render_template(
			'graveyard.html', 
			graveyard=graveyard,
			demo = "DEMO " if is_demo else ""
		)
	except Exception as e:
		db.rollback()
		return str(e) + ". Failed to load graveyard tab.", 500
	finally:
		db.close()


@app.route('/todo', methods=['GET'])
def todo_content():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		todo_unformatted = get_todo(db, is_demo)
		todo = format_todo(todo_unformatted)
		return render_template(
			'todo.html', 
			todo=todo,
			demo = "DEMO " if is_demo else ""
		)
	except Exception as e:
		db.rollback()
		return str(e) + ". Failed to load bugs tab.", 500
	finally:
		db.close()


@app.route('/bugs', methods=['GET'])
def bugs_content():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		bugs = get_bugs(db, is_demo)
		return render_template(
			'bugs.html', 
			bugs=bugs,
			demo = "DEMO " if is_demo else "",
			url_suffix = url_suffix
		)
	except Exception as e:
		db.rollback()
		return str(e) + ". Failed to load bugs tab.", 500
	finally:
		db.close()

	
@app.route('/add_bug', methods=['POST'])
def report_bug():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		description = request.form.get('description')
		added_by = request.form.get('added_by')
		add_bug(db, description, added_by, is_demo)
		# Get updated bugs list and render template
		bugs = get_bugs(db, is_demo)
		html = render_template(
			'bugs.html', 
			bugs=bugs,
			demo="DEMO " if is_demo else "",
			url_suffix=url_suffix
		)
		return jsonify({'html': html, 'close_modal': True})
	except Exception as e:
		db.rollback()
		return jsonify({'error': str(e)}), 500
	finally:
		db.close()


@app.route('/delete_bug_id', methods=['POST'])
def delete_bug():
	url_suffix = request.args.get('url_suffix', '')
	db: Session = SessionLocal()
	is_demo = True if not url_suffix or url_suffix != current_url_suffix else False
	try:
		bug_id = int(request.form.get('bug_id'))
		delete_bug_id(db, bug_id, is_demo)
		# Get updated bugs list and render template
		bugs = get_bugs(db, is_demo)
		html = render_template('bugs.html',
			bugs=bugs,
			demo="DEMO " if is_demo else "",
			url_suffix=url_suffix
		)
		return jsonify({'html': html})
	except Exception as e:
		db.rollback()
		return jsonify({'error': str(e)}), 500
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

def renderSyllabus( db, is_demo, url_suffix):
	syllabus = get_syllabus(db, is_demo)
	columns = get_columns(db, is_demo)
	pretty_columns = get_pretty_columns(db)
	assignment = get_current_assignment(db, is_demo)
	html = render_template('syllabus.html',
		syllabus=syllabus, 
		columns=columns, 
		pretty_columns=pretty_columns,
		assignment=assignment,
		demo="DEMO " if is_demo else "",
		url_suffix=url_suffix
	)
	return jsonify({'html': html, 'close_modal': True})

# TODO: 
# make actual CRUD for all of the tables
# 	Create -post
# 	read - get
# 	update - put
# 	delete - delete