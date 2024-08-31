def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Rapid Reading Homework" in rv.data
    assert b'id="syllabus-tab"' in rv.data
    assert b'id="graveyard-tab"' in rv.data
    assert b'id="todo-tab"' in rv.data
    assert b'id="bugs-tab"' in rv.data
    assert b'id="tab-content-container"' in rv.data


def test_syllabus_content(client):
    rv = client.get("/syllabus")
    assert rv.status_code == 200
    assert b"Current assignment" in rv.data
    # look for each form button
    assert b"New Assignment" in rv.data
    assert b"Add New" in rv.data
    assert b"View Less" in rv.data
    assert b"Mark Book Complete" in rv.data
    assert b"Edit" in rv.data
    assert b"Delete" in rv.data
    assert b'id="newEntryForm"' in rv.data
    assert b'id="editEntryForm"' in rv.data
    assert b'id="confirmDeleteForm"' in rv.data
    assert b'id="newAssignmentForm"' in rv.data


def test_new_assignment(client):
    data = {"assignment_data": "Read Chapter 5"}
    rv = client.post("/assign", data=data, follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/syllabus")
    assert rv.status_code == 200
    assert b"Read Chapter 5" in rv.data


def test_add_new(client):
    data = {
        "book": "New Book Title test",
        "author": "Author Name test",
        "series": "Series Name test",
        "added_by": "Tester test",
        "season": 1,
        "genre": "Fiction",
        "num_in_series": 1,
        "is_extra_credit": "on",
    }
    rv = client.post("/add", data=data, follow_redirects=True)
    assert b"New Book Title test" in rv.data
    assert b"Author Name test" in rv.data
    assert b"Series Name test" in rv.data


def test_edit_entry(client):
    # Fetch the syllabus page to find the unique_id of the added entry
    rv = client.get("/syllabus")
    assert b"New Book Title test" in rv.data
    data = rv.data.decode("utf-8")
    start_index = data.find("New Book Title test")
    if start_index == -1:
        raise AssertionError(
            "The added book entry was not found in the syllabus"
        )

    # Find the corresponding unique_id for the added entry
    unique_id_start = data.rfind("col-unique_id", 0, start_index)
    unique_id_value_start = (
        data.find('unique_id">', unique_id_start) + len('unique_id">')
    )
    unique_id_value_end = data.find("<", unique_id_value_start)
    unique_id = data[unique_id_value_start:unique_id_value_end].strip()

    # Data to be submitted for editing the entry
    data_edit = {
        "unique_id": unique_id,
        "book": "Edited Book Title test",
        "author": "Edited Author test",
        "series": "Edited Series test",
        "added_by": "Editor test",
        "season": 2,
        "num_in_series": 2,
        "is_extra_credit": "off",
        "is_completed": "on",
        "date_completed": "2023-01-01",
        "up_votes": 10,
        "down_votes": 0,
        "genre": "Non-fiction",
    }

    # Post the edit data to the /update route
    rv = client.post("/update", data=data_edit, follow_redirects=True)

    # Check if the edited entry is now on the syllabus page
    assert b"Edited Book Title test" in rv.data
    assert b"Edited Author test" in rv.data
    assert b"Edited Series test" in rv.data
    assert b"Editor test" in rv.data
    assert b"2023-01-01" in rv.data
    assert b"10" in rv.data
    assert b"Non-fiction" in rv.data


def test_complete_entry(client):
    # Assume 'Edited Book Title test' entry already exists
    rv = client.get("/syllabus")
    data = rv.data.decode("utf-8")
    start_index = data.find("Edited Book Title test")
    if start_index == -1:
        raise AssertionError(
            "The edited book entry was not found in the syllabus"
        )

    # Find the form for marking the book as complete
    form_start = data.find("<form", start_index)
    form_end = data.find("</form>", form_start) + len("</form>")
    form_content = data[form_start:form_end]

    # Extract necessary data from the form
    book_value_start = (
        form_content.find('value="') + len('value="')
    )
    book_value_end = form_content.find('"', book_value_start)
    book_name = form_content[book_value_start:book_value_end]

    # Data to be submitted for marking the book complete
    data_complete = {"book": book_name}

    # Post the complete data to the /complete route
    rv = client.post("/complete", data=data_complete, follow_redirects=True)

    # Check if the 'Mark Book Complete' button is no longer on the
    # syllabus page for the completed entry
    rv = client.get("/syllabus")
    data = rv.data.decode("utf-8")
    assert f"Edited Book Title test".encode() in rv.data
    # Ensure the 'Mark Book Complete' button is not present
    today = datetime.now().strftime("%Y-%m-%d")
    table_value_start = data.find("Edited Book Title test")
    table_value_end = data.find("Non-fiction")
    assert f"{today}".encode() in rv.data[table_value_start:table_value_end]


def test_delete_entry(client):
    # Assume 'Edited Book Title test' entry already exists and
    # find its unique_id
    rv = client.get("/syllabus")
    data = rv.data.decode("utf-8")
    start_index = data.find("Edited Book Title test")
    if start_index == -1:
        raise AssertionError(
            "The edited book entry was not found in the syllabus"
        )

    # Find the corresponding unique_id for the edited entry
    unique_id_start = data.rfind("col-unique_id", 0, start_index)
    unique_id_value_start = (
        data.find('unique_id">', unique_id_start) + len('unique_id">')
    )
    unique_id_value_end = data.find("<", unique_id_value_start)
    unique_id = data[unique_id_value_start:unique_id_value_end].strip()

    # Data to be submitted for deleting the entry
    data_delete = {"unique_id": unique_id}

    # Post the delete data to the /delete route
    rv = client.post("/delete", data=data_delete, follow_redirects=True)
    assert rv.status_code == 200

    # Check if the deleted entry is no longer on the syllabus page
    rv = client.get("/syllabus")
    assert rv.status_code == 200
    assert b"Edited Book Title test" not in rv.data
    assert b"Edited Author test" not in rv.data
    assert b"Edited Series test" not in rv.data
    assert b"Editor test" not in rv.data


def test_graveyard_content(client):
    rv = client.get("/graveyard")
    assert rv.status_code == 200
    assert b"<p>The following assignments have already been completed:</p>"
    in rv.data


def test_todo_content(client):
    rv = client.get("/todo")
    assert rv.status_code == 200
    assert b"<p>The following assignments have yet to be completed:</p>"
    in rv.data


def test_bugs_content(client):
    rv = client.get("/bugs")
    assert rv.status_code == 200
    assert b"BUGS & FEATURE REQUESTS" in rv.data
    assert b"New Bug" in rv.data


def test_add_bug(client):
    # Data to be submitted for creating a new bug report
    data = {"description": "New Bug Report test", "added_by": "Tester test"}

    # Post the data to the /add_bug route
    rv = client.post("/add_bug", data=data, follow_redirects=True)
    assert rv.status_code == 200

    # Check if the new bug report is now on the bugs page
    rv = client.get("/bugs")
    assert rv.status_code == 200
    assert b"New Bug Report test" in rv.data
    assert b"Tester test" in rv.data


def test_delete_bug(client):
    # Assume 'New Bug Report test' bug already exists and find its bug_id
    rv = client.get("/bugs")
    assert rv.status_code == 200
    data = rv.data.decode("utf-8")
    start_index = data.find("New Bug Report test")
    if start_index == -1:
        raise AssertionError(
            "The 'New Bug Report test' entry was not found in the bugs"
        )

    # Find the corresponding bug_id for the bug entry
    bug_id_start = data.rfind('name="bug_id"', 0, start_index)
    bug_id_value_start = (
        data.find('value="', bug_id_start) + len('value="')
    )
    bug_id_value_end = data.find('"', bug_id_value_start)
    bug_id = data[bug_id_value_start:bug_id_value_end]

    # Data to be submitted for deleting the bug entry
    data_delete = {"bug_id": bug_id}

    # Post the delete data to the /delete_bug_id route
    rv = client.post("/delete_bug_id", data=data_delete, follow_redirects=True)
    assert rv.status_code == 200

    # Check if the deleted entry is no longer on the bugs page
    rv = client.get("/bugs")
    assert rv.status_code == 200
    assert b"New Bug Report test" not in rv.data
    assert b"Tester test" not in rv.data


# run with pytest --disable-warnings