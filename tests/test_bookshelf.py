from django.contrib.auth.models import User
from django.test.client import Client
from django.utils import simplejson as json

from codenode.frontend.bookshelf import models
from codenode.frontend.bookshelf import views

# this stores fixture data
f = {}


def setup():
    f['user1'] = User.objects.get(username__exact='test')
    f['user2'] = User.objects.get(username__exact='test2')

def teardown():
    f = {}

def test_add_folder():
    folder = models.Folder(owner=f['user1'], title="test_folder1")
    folder.save()

    # login 
    c = Client()
    logged_in = c.login(username='test', password='password')
    assert logged_in
    
    # check if new folder was saved and we can access it
    response = c.get('/bookshelf/folders')
    resp = json.loads(response.content)
    assert response.status_code == 200
    assert resp[0][1] == "test_folder1"

