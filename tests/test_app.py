import pytest

def test_index(client):
	rv = client.get('/')
	assert rv.status_code == 200
	assert b'Syllabus' in rv.data

def test_syllabus_content(client):
	rv = client.get('/syllabus')
	assert rv.status_code == 200
	# Add more specific assertions based on expected content

# if i need to use the dev url, then I should use os.getenv('REPL_URL')