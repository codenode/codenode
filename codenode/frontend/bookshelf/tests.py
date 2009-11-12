from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from django.utils import simplejson as json

from codenode.frontend.bookshelf import models
from codenode.frontend.bookshelf import views


class TestBookshelf(TestCase):

    def setUp(self):
        
        for user in [User(username='test'), User(username='test2')]:
            user.set_password('password')
            user.save()
        self.user1 = User.objects.get(username__exact='test')
        self.user2 = User.objects.get(username__exact='test2')

    def tearDown(self):
        f = {}
        allfolders = models.Folder.objects.all()
        for folder in allfolders:
            folder.delete()

    def test_add_folder(self):
        folder = models.Folder(owner=self.user1, title="test_folder1")
        folder.save()

        # login 
        logged_in = self.client.login(username='test', password='password')
        assert logged_in
    
        # check if new folder was saved and we can access it
        response = self.client.get('/bookshelf/folders')
        resp = json.loads(response.content)
        assert response.status_code == 200
        assert resp[0][1] == "test_folder1"
        folder.delete() #clean up

