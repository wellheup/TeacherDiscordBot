import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, Mock
from commands.add import add
from commands.assign import assign
from commands.assignment import assignment
from commands.cmds import cmds
from commands.columns import columns
from commands.complete import complete
from commands.graveyard import graveyard
from commands.list_series import list_series
from commands.remove import remove
from commands.report_bug import report_bug
from commands.syllabus import syllabus
from commands.todo import todo
from commands.update_assignment import update_assignment
from commands.update import update, update_id
from commands.url import url
from utils import get_current_url
import re

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_add_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock the parameters
    book_name = "Test Book"
    author_name = "Test Author"
    series_name = "Test Series"
    season_number = 1

    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.add.SessionLocal", return_value=Mock())

    # Mock the add_book function
    mock_add_book = mocker.patch("commands.add.add_book", return_value=Mock(book=book_name))

    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.add.send_and_delete", new_callable=AsyncMock)

    # Call the add command
    await add(mock_ctx, book_name, author_name, series_name, season_number)

    # Assertions
    mock_add_book.assert_called_once_with(
        mock_db_session(),
        book_name,
        author_name,
        series_name,
        "Tester",  # This is ctx.author.name
        season_number,
        True,  # since "demo" is in ctx.channel.name
        genre=None,
        is_extra_credit=False,
    )
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, f"Added {book_name} to the syllabus")

@pytest.mark.asyncio
async def test_assign_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock the parameters
    description = "Test Assignment"

    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.assign.SessionLocal", return_value=Mock())

    # Mock the add_assignment function
    mock_add_assignment = mocker.patch("commands.assign.add_assignment", return_value=Mock(description=description))

    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.assign.send_and_delete", new_callable=AsyncMock)

    # Call the assign command
    await assign(mock_ctx, description)

    # Assertions
    mock_add_assignment.assert_called_once_with(
        mock_db_session(),
        description,
        True  # since "demo" is in ctx.channel.name
    )
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, f"The new assignment is: {description}")

@pytest.mark.asyncio
async def test_assignment_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock the parameters
    is_demo = True
    assignment_description = "Current Assignment"
    assignment_date_added = "2023-10-10"

    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.assignment.SessionLocal", return_value=Mock())

    # Mock the check_table_existing function
    mock_check_table_existing = mocker.patch("commands.assignment.check_table_existing", return_value=True)

    # Mock the get_current_assignment function
    mock_get_current_assignment = mocker.patch(
        "commands.assignment.get_current_assignment",
        return_value=Mock(description=assignment_description, date_added=assignment_date_added)
    )

    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.assignment.send_and_delete", new_callable=AsyncMock)

    # Call the assignment command
    await assignment(mock_ctx)

    # Assertions
    mock_check_table_existing.assert_called_once_with(mock_db_session(), "demo_assignments")
    mock_get_current_assignment.assert_called_once_with(mock_db_session(), True)  # since "demo" is in ctx.channel.name
    expected_message = f"The current assignment is: {assignment_description}, assigned on {assignment_date_added}"
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, expected_message)

@pytest.mark.asyncio
async def test_cmds_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.cmds.send_and_delete", new_callable=AsyncMock)

    # Import command_descriptions from cmds.py
    from commands.cmds import command_descriptions

    # Call the cmds command
    await cmds(mock_ctx)

    # Assertions
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, command_descriptions)

@pytest.mark.asyncio
async def test_columns_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"
    # Mock the expected column names returned by the get_columns function
    mock_columns = [
        'unique_id', 'book', 'author', 'series', 'num_in_series', 'date_added',
        'is_completed', 'added_by', 'season', 'is_extra_credit', 'date_completed',
        'up_votes', 'down_votes', 'genre'
    ]
    # Mock get_columns function
    mock_get_columns = mocker.patch("commands.columns.get_columns", return_value=mock_columns)
    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.columns.send_and_delete", new_callable=AsyncMock)
    # Call the columns command
    await columns(mock_ctx)
    # Build the expected message
    expected_message = "Column names in the syllabus table:\n- " + "\n- ".join(mock_columns)
    # Assertions
    mock_get_columns.assert_called_once_with(mocker.ANY, True)  # pass db_session and is_demo
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, expected_message)

@pytest.mark.asyncio
async def test_complete_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock the parameters
    item_name_or_id = "Test Book"
    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.complete.SessionLocal", return_value=Mock())
    # Mock the complete_book function
    mock_complete_book = mocker.patch("commands.complete.complete_book", return_value=Mock(book=item_name_or_id))
    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.complete.send_and_delete", new_callable=AsyncMock)
    # Call the complete command
    await complete(mock_ctx, item_name_or_id)
    # Assertions
    mock_complete_book.assert_called_once_with(
        mock_db_session(),
        item_name_or_id,
        True  # since "demo" is in ctx.channel.name
    )
    # Expected message
    expected_message = "Marked Test Book as completed"
    # Check if actual message matches the expected message without the period
    actual_message = mock_send_and_delete.await_args[0][1]
    assert actual_message == expected_message, f"Actual message '{actual_message}' does not match expected message '{expected_message}'"
    # Ensure it was awaited once
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, expected_message)
    
@pytest.mark.asyncio
async def test_graveyard_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock the parameters
    minutes = 5

    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.graveyard.SessionLocal", return_value=Mock())

    # Mock the get_graveyard_bot function
    mock_get_graveyard_bot = mocker.patch("commands.graveyard.get_graveyard_bot", return_value=[
        ("Book1", "Author1", "Series1", 1, "ID1", 1),
        ("Book2", "Author2", "", 2, "ID2", 1)
    ])

    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.graveyard.send_and_delete", new_callable=AsyncMock)

    # Call the graveyard command
    await graveyard(mock_ctx, minutes)

    # Assertions
    mock_get_graveyard_bot.assert_called_once_with(mock_db_session(), True)  # since "demo" is in ctx.channel.name
    expected_message = """**The following assignments have already been completed: **
**Author1**
- Series1
  - *Book1* ✅ (ID1)
**Author2**
- *Book2* ✅ (ID2)
"""
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, expected_message)

@pytest.mark.asyncio
async def test_list_series_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock the parameters
    series_name = "Test Series"

    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.list_series.SessionLocal", return_value=Mock())

    # Mock the get_series function
    mock_get_series = mocker.patch("commands.list_series.get_series", return_value=[
        ("Book1", "Author1", series_name, 1),
        ("Book2", "Author1", series_name, 2)
    ])

    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.list_series.send_and_delete", new_callable=AsyncMock)

    # Call the list_series command
    await list_series(mock_ctx, series_name)

    # Assertions
    mock_get_series.assert_called_once_with(mock_db_session(), series_name, True)  # since "demo" is in ctx.channel.name
    expected_message = """Test Series by **Author1**
1.  *Book1*
2.  *Book2*
"""
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, expected_message)

@pytest.mark.asyncio
async def test_remove_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"
    # Mock the parameters
    book_or_id = "Test Book"
    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.remove.SessionLocal", return_value=Mock())
    # Mock the remove_book and remove_id functions
    mock_remove_book = mocker.patch("commands.remove.remove_book", return_value=Mock(book=book_or_id))
    mock_remove_id = mocker.patch("commands.remove.remove_id", return_value=Mock(book="123"))
    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.remove.send_and_delete", new_callable=AsyncMock)
    # Call the remove command with a book name
    await remove(mock_ctx, book_or_id)
    mock_remove_book.assert_called_once_with(mock_db_session(), book_or_id, True)
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, f"Removed {book_or_id} from the syllabus")
    # Reset mock calls
    mock_remove_book.reset_mock()
    mock_send_and_delete.reset_mock()
    # Call the remove command with an ID
    book_id = "123"
    await remove(mock_ctx, book_id)
    mock_remove_id.assert_called_once_with(mock_db_session(), book_id, True)
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, f"Removed 123 from the syllabus")

@pytest.mark.asyncio
async def test_report_bug_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock the parameters
    description = "Test Bug"

    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.report_bug.SessionLocal", return_value=Mock())

    # Mock the add_bug function
    mock_add_bug = mocker.patch("commands.report_bug.add_bug")

    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.report_bug.send_and_delete", new_callable=AsyncMock)

    # Call the report_bug command
    await report_bug(mock_ctx, description)

    # Assertions
    mock_add_bug.assert_called_once_with(mock_db_session(), description, "Tester", True)  # since "demo" is in ctx.channel.name
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, "Bug report submitted successfully! Thank you for your feedback.")

@pytest.mark.asyncio
async def test_syllabus_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"

    # Mock the parameters
    minutes = 5

    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.syllabus.SessionLocal", return_value=Mock())
    # Mock get_syllabus function
    mock_get_syllabus_bot = mocker.patch("commands.syllabus.get_syllabus_bot", return_value=[
        ("Book1", "Author1", "Series1", 1, "ID1", False),
        ("Book2", "Author2", "", 2, "ID2", False)
    ])
    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.syllabus.send_and_delete", new_callable=AsyncMock)
    # Call the syllabus command
    await syllabus(mock_ctx, minutes)
    # Assertions
    mock_get_syllabus_bot.assert_called_once_with(mock_db_session(), True)  # since "demo" is in ctx.channel.name
    expected_message = """**The current syllabus is as follows: **
**Author1**
- Series1
  - *Book1* (ID1)
**Author2**
- *Book2* (ID2)
"""
    pattern = re.compile(r'\s+')
    clean_expected_message = re.sub(pattern, '', expected_message)
    clean_actual_message = re.sub(pattern, '', mock_send_and_delete.await_args[0][1])
    assert clean_actual_message == clean_expected_message, f"Actual message '{clean_actual_message}' does not match expected message '{clean_expected_message}'"

@pytest.mark.asyncio
async def test_todo_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"
    # Mock the parameters
    minutes = 5
    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.todo.SessionLocal", return_value=Mock())
    # Mock get_todo function
    mock_get_todo = mocker.patch("commands.todo.get_todo", return_value=[
        ("Book1", "Author1", "Series1", 1, "ID1", False),
        ("Book2", "Author2", "", 2, "ID2", False)
    ])
    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.todo.send_and_delete", new_callable=AsyncMock)
    # Call the todo command
    await todo(mock_ctx, minutes)
    # Assertions
    mock_get_todo.assert_called_once_with(mock_db_session(), True)  # since "demo" is in ctx.channel.name
    expected_message = """**The following assignments have not yet been completed: **
**Author1**
- Series1
  - *Book1* (ID1)
**Author2**
- *Book2* (ID2)
"""
    pattern = re.compile(r'\s+')
    clean_expected_message = re.sub(pattern, '', expected_message)
    clean_actual_message = re.sub(pattern, '', mock_send_and_delete.await_args[0][1])

    assert clean_actual_message == clean_expected_message, f"Actual message '{clean_actual_message}' does not match expected message '{clean_expected_message}'"

@pytest.mark.asyncio
async def test_update_assignment_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"
    # Mock the parameters
    description = "Updated Assignment"
    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.update_assignment.SessionLocal", return_value=Mock())
    # Mock update_current_assignment function
    mock_update_current_assignment = mocker.patch("commands.update_assignment.update_current_assignment")

    # Set return values for the mock
    mock_update_current_assignment.return_value.description = description
    mock_update_current_assignment.return_value.date_added = None
    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.update_assignment.send_and_delete", new_callable=AsyncMock)
    # Call the update_assignment command
    await update_assignment(mock_ctx, description)
    # Assertions
    mock_update_current_assignment.assert_called_once_with(mock_db_session(), description, True)  # since "demo" is in ctx.channel.name
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, f"The current assignment is now: {description}, assigned on None")

@pytest.mark.asyncio
async def test_update_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"
    # Mock parameters
    item_name_or_id = "Test Book"
    column_name = "Column1"
    new_value = "New Value"
    # Mock the database session and methods
    mock_db_session = mocker.patch("commands.update.SessionLocal", return_value=Mock())
    # Mock update_book and update_id functions
    mock_update_book = mocker.patch("commands.update.update_book", return_value=Mock(book=item_name_or_id))
    mock_update_id = mocker.patch("commands.update.update_id", return_value=Mock(book=item_name_or_id))
    # Mock send_and_delete
    mock_send_and_delete = mocker.patch("commands.update.send_and_delete", new_callable=AsyncMock)
    # Call the update command
    await update(mock_ctx, item_name_or_id, column_name, new_value)
    # Assertions
    if item_name_or_id.isdigit() and int(item_name_or_id) > 0:
        mock_update_id.assert_called_once_with(mock_db_session(), item_name_or_id, column_name, new_value, True)  # since "demo" is in ctx.channel.name
    else:
        mock_update_book.assert_called_once_with(mock_db_session(), item_name_or_id, column_name, new_value, True)
    mock_send_and_delete.assert_awaited_once_with(mock_ctx, f"Updated {item_name_or_id} in column {column_name} with value {new_value}")

@pytest.mark.asyncio
async def test_url_command(mocker):
    # Create a mock context
    mock_ctx = Mock()
    mock_ctx.author.name = "Tester"
    mock_ctx.channel.name = "demo-channel"
    # Mock ctx.send
    mock_ctx.send = AsyncMock()
    # Call the url command
    await url(mock_ctx)
    # Assertions
    mock_ctx.send.assert_awaited_once_with(f"The current URL is: {get_current_url(True)}")