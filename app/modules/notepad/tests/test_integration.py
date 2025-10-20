from app import db
from app.modules.notepad.models import Notepad
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app.modules.profile.models import UserProfile

import pytest


from app import db
from app.modules.notepad.models import Notepad
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app.modules.profile.models import UserProfile

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()


    yield test_client

def test_index_returns_notepads(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    response = test_client.get('/notepad')
    assert response.status_code == 200, "Notepad index page did not load successfully."
    
    logout(test_client)
    
def test_list_empty_notepad_get(test_client):
    """
    Tests access to the empty notepad list via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"You have no notepads." in response.data, "The expected content is not present on the page"

    logout(test_client)
    
def test_create_notepad(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    response = test_client.post(
        '/notepad/create',
        data={'title': 'Aprender testing', 'body': 'Contenido de prueba'},
        follow_redirects=True
    )
    assert response.status_code == 200, "La creación del notepad no devolvió 200."


    user = User.query.filter_by(email="user@example.com").first()
    assert user is not None, "Usuario de prueba no encontrado en la BD."

    new_notepad = Notepad.query.filter_by(title="Aprender testing", user_id=user.id).first()
    assert new_notepad is not None, "No se creó el Notepad en la base de datos."
    assert new_notepad.body == "Contenido de prueba"
    logout(test_client)
    
    
def test_get_notepad_by_id_(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    user = User.query.filter_by(email="user@example.com").first()
    notepad = Notepad(title="Leer por id", body="Cuerpo lectura", user_id=user.id)
    db.session.add(notepad)
    db.session.commit()

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200

    response = test_client.get(f'/notepad/{notepad.id}')
    assert response.status_code == 200
    assert "Leer por id" in response.data.decode()

    db.session.delete(notepad)
    db.session.commit()
    logout(test_client)


def test_edit_notepad_get_and_post_updates(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    user = User.query.filter_by(email="user@example.com").first()
    notepad = Notepad(title="Para editar", body="Antes", user_id=user.id)
    db.session.add(notepad)
    db.session.commit()

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200

  
    get_resp = test_client.get(f'/notepad/edit/{notepad.id}')
    assert get_resp.status_code == 200
    assert "Para editar" in get_resp.data.decode()

   
    post_resp = test_client.post(
        f'/notepad/edit/{notepad.id}',
        data={'title': 'Editado', 'body': 'Después'},
        follow_redirects=True
    )
    assert post_resp.status_code == 200

    updated = Notepad.query.get(notepad.id)
    assert updated.title == "Editado"
    assert updated.body == "Después"
    
    db.session.delete(updated)
    db.session.commit()
    logout(test_client)

def test_delete_notepad_authorized_and_unauthorized(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    user = User.query.filter_by(email="user@example.com").first()

    n1 = Notepad(title="Borrar yo", body="Borrar", user_id=user.id)
    db.session.add(n1)
    db.session.commit()

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200

    del_resp = test_client.post(f'/notepad/delete/{n1.id}', follow_redirects=True)
    assert del_resp.status_code == 200
    assert Notepad.query.get(n1.id) is None
    logout(test_client)