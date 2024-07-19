from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from crud import *
import os

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
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
	db: Session = SessionLocal()
	is_demo = False if os.getenv('REPLIT_DEPLOYMENT') == '1' else True
	syllabus = get_syllabus_all(db, is_demo)
	columns = get_columns(db, is_demo)
	pretty_columns = get_pretty_columns(db)
	bugs = get_bugs(db, is_demo)
	assignment = get_current_assignment(db, is_demo)
	return render_template('index.html', syllabus=syllabus, columns = columns, pretty_columns = pretty_columns, bugs = bugs, assignment = assignment)

@app.route('/update', methods=[ 'POST'])
def update():
	db: Session = SessionLocal()
	is_demo = False if os.getenv('REPLIT_DEPLOYMENT') == '1' else True
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
		return redirect(url_for('index'))

	except Exception as e:
		db.rollback()
		return str(e) + ". Failed to post data.", 500
	finally:
		db.close()

@app.route('/add', methods=['POST'])
def add():
	db: Session = SessionLocal()
	is_demo = False if os.getenv('REPLIT_DEPLOYMENT') == '1' else True
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

		return redirect(url_for('index'))
		
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()


@app.route('/delete', methods=['POST'])
def delete():
	db: Session = SessionLocal()
	is_demo = False if os.getenv('REPLIT_DEPLOYMENT') == '1' else True
	try:
		id = int(request.form.get('unique_id'))
		remove_id(db, id, is_demo)
		return redirect(url_for('index'))
	except Exception as e:
		db.rollback()
		return str(e), 500
	finally:
		db.close()

@app.route('/assign', methods=['POST'])
def assign():
    db: Session = SessionLocal()
    is_demo = False if os.getenv('REPLIT_DEPLOYMENT') == '1' else True
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        print("in assign")
        assignment_data = request.form.get('assignment_data')
        add_assignment(db, assignment_data, date, is_demo)
        return redirect(url_for('index'))
    except Exception as e:
        db.rollback()
        return str(e), 500
    finally:
        db.close()

@app.route('/bug', methods=['POST'])
def report_bug():
    db: Session = SessionLocal()
    is_demo = False if os.getenv('REPLIT_DEPLOYMENT') == '1' else True
    try:
        description = request.form.get('description')
        print(f"description: {description}")
        added_by = request.form.get('added_by')
        print(f"added_by: {added_by}")
        add_bug(db, description, added_by, is_demo)
        return redirect(url_for('index'))
    except Exception as e:
        db.rollback()
        return str(e), 500
    finally:
        db.close()

# TODO: 
# add a graveyard tab
# add a series list tab
# add a todo page
# add a complete button for each assignment
# add a delete button for bugs
# add an "are you sure you want to delete this?" popup for bugs