from flaskr import backend
from flaskr import create_app
import pytest 
from unittest.mock import patch, mock_open
from unittest.mock import MagicMock
from flask import Flask, flash, request, redirect, url_for
#from flaskr.pages.py import make_endpoints
# TODO(Project 1): Write tests for Backend methods.
"""
app =Flask(__name__)


class mockBakend:
    def __init__(self,plst,wikip):
        self.mockbuccket = "bmocked"
        self.pageslist = ["somehome", "abouthello","name of another page"]

mock_wiki_page = "Here is the info if this was a wiki page"
mock_pages = ["somehome", "abouthello","name of another page"]
backmock = backend.mockBackend(mock_pages,mock_wiki_page)
def test_get_wiki():
    with patch("builtins.open", mock_open(read_data=mock_wiki_page)) as mock_file:
        with make_endpoints(app) as pages:
            content = backmock.get_wiki_page(mock_wiki_page)
        assert content == "Here is the info if this was a wiki page"

def test_all_wikipages():
        with patch("builtins.open", mock_open(read_data=mock_pages)) as mock_file:
            with make_endpoints(app) as pages:
                listp = backmock.get_all_page_names()
        assert listp == "Here is the info if this was a wiki page"

"""