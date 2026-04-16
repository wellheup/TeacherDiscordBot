from sqlalchemy import Boolean, Column, Date, Integer, String, text

from database import Base, engine


class Syllabus(Base):
        __tablename__ = "syllabus"

        unique_id = Column(Integer, primary_key=True, index=True)
        book = Column(String, index=True)
        author = Column(String, index=True)
        series = Column(String, index=True, nullable=True, default="")
        num_in_series = Column(Integer, index=True, nullable=True)
        date_added = Column(Date)
        is_completed = Column(Boolean, default=False)
        added_by = Column(String)
        season = Column(Integer, index=True, default=None)
        is_extra_credit = Column(Boolean, default=False)
        date_completed = Column(Date)
        up_votes = Column(Integer, default=0)
        down_votes = Column(Integer, default=0)
        genre = Column(String, default="")


class Bugs(Base):
        __tablename__ = "bugs"

        bug_id = Column(Integer, primary_key=True, index=True)
        description = Column(String, index=True)
        added_by = Column(String)


class Assignments(Base):
        __tablename__ = "assignments"

        assignment_id = Column(Integer, primary_key=True, index=True)
        description = Column(String, index=True)
        date_added = Column(Date)
        due_date = Column(Date, nullable=True)


class DemoSyllabus(Base):
        __tablename__ = "demo_syllabus"

        unique_id = Column(Integer, primary_key=True, index=True)
        book = Column(String, index=True)
        author = Column(String, index=True)
        series = Column(String, index=True, nullable=True, default="")
        num_in_series = Column(Integer, index=True, nullable=True)
        date_added = Column(Date)
        is_completed = Column(Boolean, default=False)
        added_by = Column(String)
        season = Column(Integer, index=True, default=None)
        is_extra_credit = Column(Boolean, default=False)
        date_completed = Column(Date)
        up_votes = Column(Integer, default=0)
        down_votes = Column(Integer, default=0)
        genre = Column(String, default="")


class DemoBugs(Base):
        __tablename__ = "demo_bugs"

        bug_id = Column(Integer, primary_key=True, index=True)
        description = Column(String, index=True)
        added_by = Column(String)


class DemoAssignments(Base):
        __tablename__ = "demo_assignments"

        assignment_id = Column(Integer, primary_key=True, index=True)
        description = Column(String, index=True)
        date_added = Column(Date)
        due_date = Column(Date, nullable=True)


class AppConfig(Base):
        __tablename__ = "app_config"

        key = Column(String, primary_key=True)
        value = Column(String)


# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Migrate: add due_date column if it doesn't exist yet
with engine.connect() as _conn:
        _conn.execute(text("ALTER TABLE assignments ADD COLUMN IF NOT EXISTS due_date DATE"))
        _conn.execute(text("ALTER TABLE demo_assignments ADD COLUMN IF NOT EXISTS due_date DATE"))
        _conn.commit()
