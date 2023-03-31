from flaskr import create_app

import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'LOGIN_DISABLED': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome To Team Kage's Amazing Project" in resp.data

# TODO(Project 1): Write tests for other routes.
"""
def test_about(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"<h3>About this Wiki</h3>" in resp.data

def test_upload(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"<h1>Upload doc to the wiki</h1>" in resp.data
    
def test_pages(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"<h3>Pages contained in this Wiki</h3>" in resp.data
"""