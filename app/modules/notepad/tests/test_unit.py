import pytest

from app import db
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app.modules.profile.models import UserProfile
from app.modules.notepad.models import Notepad
from unittest.mock import MagicMock

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client

def test_edit_profile_page_get(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/profile/edit")
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Edit profile" in response.data, "The expected content is not present on the page"

    logout(test_client)

def test_create_note(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200

    response = test_client.post(
        '/notepad/create',
        data={'title': 'Test Note', 'body': 'This is a test note.'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Test Note' in response.data

    logout(test_client)

def test_list_notes(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get('/notepad')
    assert response.status_code == 200
    assert b'Test Note' in response.data

def test_update_note(test_client):
    note = Notepad.query.filter_by(title='Test Note').first()
    response = test_client.post(f'/notepad/edit/{note.id}', data={'title': 'Updated Note', 'content': 'Updated content.'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Note' in response.data

def test_delete_note(test_client):
    note = Notepad.query.filter_by(title='Updated Note').first()
    response = test_client.post(f'/notepad/delete/{note.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Note' not in response.data

def test_note_access_requires_login(test_client):
    response = test_client.get('/notepad', follow_redirects=True)
    assert response.status_code != 404

## Test unitarios
def test_notepad_model_repr():
    note = Notepad(id=1, title="Test Note", body="This is a test note.", user_id=1)
    note.user = MagicMock(username="testuser")
    assert repr(note) == "Notepad<1, Title=Test Note, Author=testuser>"