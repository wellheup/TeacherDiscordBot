from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import (Column, Integer, String, Text, MetaData, Table, inspect)
from models import Syllabus
from models import Bugs
from models import Assignments
from models import DemoSyllabus
from models import DemoBugs
from models import DemoAssignments
from datetime import datetime

def add_assignment(db: Session, description: str, is_demo: bool):
	date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		if is_demo:
			db_assignment = DemoAssignments(description=description, date_added=date)
		else:
			db_assignment = Assignments(description=description, date_added=date)
		db.add(db_assignment)
		db.commit()
		db.refresh(db_assignment)
		return db_assignment
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error adding assignment: {e}")        
		raise


def create_assignments_table(db: Session, table_name: str):
	try:
		metadata = MetaData(bind=db.bind)
		inspector = inspect(db.bind)
		if not inspector.has_table(table_name):
			assignments_table = Table(
				table_name,
				metadata,
				Column('assignment_id', Integer, primary_key=True, autoincrement=True),
				Column('description', Text, nullable=False),
				Column('date_added', Date, nullable=False),
			)
			metadata.create_all()
			print(f"'{table_name}' table created")
		else:
			print(f"'{table_name}' table already exists")
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error creating new assignments table: {e}")
		raise
		


def add_book(db: Session, 
			book: str, 
			author: str, 
			series: str, 
			added_by: str, 
			season: int = 0,
			is_demo: bool = True, 
			genre: str = "",
			num_in_series: int = None,
			is_extra_credit: bool = False):
	date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		if is_demo:
			db_book = DemoSyllabus(book=book, author=author, series=series, added_by=added_by, num_in_series=num_in_series, genre=genre, season=season, is_extra_credit=is_extra_credit, date_added=date)
		else:
			db_book = Syllabus(book=book, author=author, series=series, added_by=added_by, num_in_series=num_in_series, genre=genre, season=season, is_extra_credit=is_extra_credit, date_added=date)
		db.add(db_book)
		db.commit()
		db.refresh(db_book)
		return db_book
	except Exception as e:
		db.rollback()  # Rollback on error
		print()
		print(f"Error adding book: {e}")
		raise


def get_current_assignment(db: Session, is_demo: bool):
	try:
		if is_demo:
			db_Assignment = db.query(DemoAssignments).order_by(DemoAssignments.assignment_id.desc()).first()
		else:
			db_Assignment = db.query(Assignments).order_by(Assignments.assignment_id.desc()).first()
		return db_Assignment
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error getting assignment: {e}")
		raise
		

def get_columns(db: Session, is_demo: bool):
	try:
		if is_demo:
			return db.query(DemoSyllabus).first().__table__.columns.keys()
		else:
			return db.query(Syllabus).first().__table__.columns.keys()
	except Exception as e:
		print(f"Error getting columns: {e}")
		raise


def get_pretty_columns(db: Session):
	columns = {
		'unique_id': 'ID', 'book': 'Book', 'author': 'Author', 'series': 'Series', 'num_in_series': 'Volume', 
		'date_added': 'Added On', 'is_completed': 'Done?', 'added_by': 'Added By', 'season': 'Season', 
		'is_extra_credit': 'Extra', 'date_completed': 'Completed On', 'up_votes': '👍', 'down_votes': '👎', 'genre': 'Genre'
	}
	return columns
	

def complete_book(db: Session, book_name: str, is_demo: bool):
	date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		if is_demo:
			db_book = db.query(DemoSyllabus).filter(DemoSyllabus.book == book_name).first()
		else:
			db_book = db.query(Syllabus).filter(Syllabus.book == book_name).first()
		db_book.is_completed = True
		db_book.date_completed = date
		db.commit()
		db.refresh(db_book)
		return db_book
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error completing book: {e}")
		raise


def delete_bug_id(db: Session, bug_id: int, is_demo: bool):
	try:
		if is_demo:
			db_bug = db.query(DemoBugs).filter(DemoBugs.bug_id == bug_id).first()
		else:
			db_bug = db.query(Bugs).filter(Bugs.bug_id == bug_id).first()
		if db_bug:
			db.delete(db_bug)
			db.commit()
			return db_bug
		return None
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error deleting bug: {e}")
		raise


def get_graveyard_bot(db: Session, is_demo: bool):
	try:
		if is_demo:
			return db.query(DemoSyllabus.book, DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series, DemoSyllabus.unique_id, DemoSyllabus.is_completed) \
				.filter(DemoSyllabus.is_completed == True) \
				.order_by(DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series) \
				.all()
		else:
			return db.query(Syllabus.book, Syllabus.author, Syllabus.series, Syllabus.num_in_series, Syllabus.unique_id, Syllabus.is_completed) \
				.filter(Syllabus.is_completed == True) \
				.order_by(Syllabus.author, Syllabus.series, Syllabus.num_in_series) \
				.all()
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error getting graveyard: {e}")
		raise


def get_graveyard_web(db: Session, is_demo: bool):
	try:
		if is_demo:
			return db.query(DemoSyllabus) \
				.filter(DemoSyllabus.is_completed == True) \
				.order_by(DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series) \
				.all()
		else:
			return db.query(Syllabus) \
				.filter(Syllabus.is_completed == True) \
				.order_by(Syllabus.author, Syllabus.series, Syllabus.num_in_series) \
				.all()
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error getting graveyard: {e}")
		raise


def get_series(db: Session, series: str, is_demo: bool):
	if is_demo:
		return db.query(DemoSyllabus.book, DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series) \
			.filter(DemoSyllabus.series == series) \
			.order_by(DemoSyllabus.num_in_series) \
			.all()
	else:
		return db.query(Syllabus.book, Syllabus.author, Syllabus.series, Syllabus.num_in_series) \
			.filter(Syllabus.series == series) \
			.order_by(Syllabus.num_in_series) \
			.all()


# def find_id(db: Session, book_id: int, is_demo: bool):
#     try: 
#         if is_demo:
#             db_book = db.query(DemoSyllabus.book).filter(DemoSyllabus.unique_id == book_id).first()
#         else:
#             db_book = db.query(Syllabus.book).filter(Syllabus.unique_id == book_id).first()
#         return db_book
#     except Exception as e:
#         db.rollback()  # Rollback on error
#         print(f"Error completing book: {e}")
#         raise

# def find_book(db: Session, book_name: str, is_demo: bool):
#     try: 
#         if is_demo:
#             db_book = db.query(DemoSyllabus.book).filter(DemoSyllabus.book == book_name).first()
#         else:
#             db_book = db.query(Syllabus.book).filter(Syllabus.book == book_name).first()
#         return db_book
#     except Exception as e:
#         db.rollback()  # Rollback on error
#         print(f"Error completing book: {e}")
#         raise

# def update_book_poll(db: Session, book_name: str, up_votes: int, down_votes: int, is_demo: bool):
#     try: 
#         if is_demo:
#             db_book = db.query(DemoSyllabus.book, DemoSyllabus.up_votes, DemoSyllabus.down_votes).filter(DemoSyllabus.book == book_name).first()
#         else:
#             db_book = db.query(Syllabus.book, Syllabus.up_votes, Syllabus.down_votes).filter(Syllabus.book == book_name).first()
#         db_book.up_votes = up_votes
#         db_book.down_votes = down_votes
#         db.commit()
#         db.refresh(db_book)
#         return db_book
#     except Exception as e:
#         db.rollback()  # Rollback on error
#         print(f"Error completing book: {e}")
#         raise

		
def remove_book(db: Session, book_name: str, is_demo: bool):
	try:
		if is_demo:
			db_book = db.query(DemoSyllabus).filter(DemoSyllabus.book == book_name).first()
		else:
			db_book = db.query(Syllabus).filter(Syllabus.book == book_name).first()
		if db_book:
			db.delete(db_book)
			db.commit()
		return db_book
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error completing book: {e}")
		raise


def remove_id(db: Session, book_id: int, is_demo: bool):
	try:
		if is_demo:
			db_book = db.query(DemoSyllabus).filter(DemoSyllabus.unique_id == book_id).first()
		else:
			db_book = db.query(Syllabus).filter(Syllabus.unique_id == book_id).first()
		if db_book:
			db.delete(db_book)
			db.commit()
		return db_book
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error completing book: {e}")
		raise

		
def add_bug(db: Session, description: str, added_by: str, is_demo: bool):
	try:
		if is_demo:
			db_bug = DemoBugs(description=description, added_by=added_by)
		else:
			db_bug = Bugs(description=description, added_by=added_by)
		db.add(db_bug)
		db.commit()
		db.refresh(db_bug)
		return db_bug
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error adding bug: {e}")
		raise


def check_table_existing(db: Session, table_name: str):
	try:
		inspector = inspect(db.bind)
		return inspector.has_table(table_name)
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error checking db for table: {e}")
		raise


def create_bugs_table(db: Session, table_name: str):
	try:
		metadata = MetaData(bind=db.bind)
		inspector = inspect(db.bind)
		if not inspector.has_table(table_name):
			bugs_table = Table(
				table_name,
				metadata,
				Column('bug_id', Integer, primary_key=True, autoincrement=True),
				Column('description', Text, nullable=False),
				Column('added_by', String(255), nullable=False),
			)
			metadata.create_all()
			print(f"'{table_name}' table created")
		else:
			print(f"'{table_name}' table already exists")
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error creating new bugs table: {e}")
		raise


def get_syllabus_bot(db: Session, is_demo: bool):
	try:
		if is_demo:
			return db.query(DemoSyllabus.book, DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series, DemoSyllabus.unique_id, DemoSyllabus.is_completed) \
				.order_by(DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series) \
				.all()
		else:
			return db.query(Syllabus.book, Syllabus.author, Syllabus.series, Syllabus.num_in_series, Syllabus.unique_id, Syllabus.is_completed) \
				.order_by(Syllabus.author, Syllabus.series, Syllabus.num_in_series) \
				.all()
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error getting syllabus: {e}")
		raise


def get_syllabus_web(db: Session, is_demo: bool):
	try:
		if is_demo:
			return db.query(DemoSyllabus) \
				.order_by(DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series) \
				.all()
		else:
			return db.query(Syllabus).order_by(Syllabus.author, Syllabus.series, Syllabus.num_in_series).all()
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error getting syllabus: {e}")
		raise


def get_todo(db: Session, is_demo: bool):
	try:
		if is_demo:
			return db.query(DemoSyllabus.book, DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series, DemoSyllabus.unique_id, DemoSyllabus.is_completed) \
				.filter(DemoSyllabus.is_completed == False) \
				.order_by(DemoSyllabus.author, DemoSyllabus.series, DemoSyllabus.num_in_series) \
				.all()
		else:
			return db.query(Syllabus.book, Syllabus.author, Syllabus.series, Syllabus.num_in_series, Syllabus.unique_id, Syllabus.is_completed) \
				.filter(Syllabus.is_completed == False) \
				.order_by(Syllabus.author, Syllabus.series, Syllabus.num_in_series) \
				.all()
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error getting graveyard: {e}")
		raise


def update_book(db: Session, book_name: str, column: str, new_value: str, is_demo: bool):
	try:
		if is_demo:
			db_book = db.query(DemoSyllabus).filter(DemoSyllabus.book == book_name).first()
		else:
			db_book = db.query(Syllabus).filter(Syllabus.book == book_name).first()
		if db_book:
			setattr(db_book, column, new_value)
			db.commit()
			db.refresh(db_book)
		return db_book
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error updating book: {e}")
		raise


def update_current_assignment(db: Session, new_value: str, is_demo: bool):
	try:
		if is_demo:
			db_Assignment = db.query(DemoAssignments).order_by(DemoAssignments.assignment_id.desc()).first()
		else:
			db_Assignment = db.query(Assignments).order_by(Assignments.assignment_id.desc()).first()
		if db_Assignment:
			db_Assignment.description = new_value
			db.commit()
			db.refresh(db_Assignment)
		return db_Assignment
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error updating assignment: {e}")
		raise


def update_id(db: Session, book_id: int, column: str, new_value: str, is_demo: bool):
	try:
		if is_demo:
			db_book = db.query(DemoSyllabus).filter(DemoSyllabus.unique_id == book_id).first()
		else:
			db_book = db.query(Syllabus).filter(Syllabus.unique_id == book_id).first()
		if db_book:
			setattr(db_book, column, new_value)
			db.commit()
			db.refresh(db_book)
			print(db_book)
		return db_book
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error updating book: {e}")
		raise


def update_database(
	db: Session, 
	unique_id: int,
	book: str, 
	author: str, 
	series: str, 
	is_completed: bool, 
	added_by: str, 
	season: int, 
	num_in_series: int,
	is_extra_credit: bool, 
	date_completed: str, 
	up_votes: int, 
	down_votes: int, 
	genre: str, 
	is_demo: bool
):
	try:
		if is_demo:
			db_book = db.query(DemoSyllabus).filter(DemoSyllabus.unique_id == unique_id).first()
		else:
			db_book = db.query(Syllabus).filter(Syllabus.unique_id == unique_id).first()
		if db_book:
			db_book.book = book
			db_book.author = author
			db_book.series = series
			db_book.is_completed = is_completed
			db_book.added_by = added_by
			db_book.season = season
			db_book.num_in_series = num_in_series
			db_book.is_extra_credit = is_extra_credit
			if date_completed:
				db_book.date_completed = date_completed
			db_book.up_votes = up_votes
			db_book.down_votes = down_votes
			db_book.genre = genre
			db.commit()
			db.refresh(db_book)
			print(db_book)
		return db_book
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error updating book: {e}")
		raise


def get_books_by_author(db: Session, author: str, is_demo: bool):
	try:
		if is_demo:
			return db.query(DemoSyllabus.series, DemoSyllabus.book) \
				.filter(DemoSyllabus.author == author) \
				.order_by(DemoSyllabus.series, DemoSyllabus.num_in_series) \
				.all()
		else:
			return db.query(Syllabus.series, Syllabus.book) \
				.filter(Syllabus.author == author) \
				.order_by(Syllabus.series, Syllabus.num_in_series) \
				.all()
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error getting books by author: {e}")
		raise


def get_bugs(db: Session, is_demo: bool):
	try:
		if is_demo:
			return db.query(DemoBugs).all()
		else:
			return db.query(Bugs).all()
	except Exception as e:
		db.rollback()  # Rollback on error
		print(f"Error getting bugs: {e}")
		raise


