import uuid

from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase

from codenode.frontend.notebook import models
from codenode.frontend.notebook import views


class TestNotebookModel(TestCase):

    def setUp(self):
        for user in [User(username='test'), User(username='test2')]:
            user.set_password('password')
            user.save()
        
        self.user1 = User.objects.get(username__exact='test')
        self.user2 = User.objects.get(username__exact='test2')

    def tearDown(self):
        f = {}
        allnotebooks = models.Notebook.objects.all()
        for nb in allnotebooks:
            nb.delete()
        allcells = models.Cell.objects.all()
        for cell in allcells:
            cell.delete()

    def test_a_new_notebook_is_assigned_a_guid(self):
        nb = models.Notebook(owner=self.user1)
        nb.save()
        assert nb.guid is not None

    def test_adding_a_cell_to_a_notebook_updates_the_last_modified_time(self):
        nb = models.Notebook(owner=self.user1)
        nb.save()
        first_time = nb.last_modified_time()
    
        print nb.created_time
    
        cell = models.Cell(
            guid=str(uuid.uuid4()).replace("-", ""), 
            notebook=nb,
            owner=nb.owner
            )
        cell.save()
    
        print nb.cell_set.all()
        print cell.last_modified
    
        second_time = nb.last_modified_time()
        assert second_time > first_time
        nb.delete() #clean up

    def test_notebook_last_modified_by_returns_last_cell_modifier(self):
        nb = models.Notebook(owner=self.user1)
        nb.save()
        assert nb.last_modified_by() == self.user1
    
        cell = models.Cell(
            guid=str(uuid.uuid4()).replace("-", ""), 
            notebook=nb,
            owner=self.user2
            )
        cell.save()
        assert nb.last_modified_by() == self.user2
        nb.delete() #clean up

    def test_view_notebook(self):
        nb = models.Notebook(owner=self.user1, title='atitle')
        nb.save()
    
        # login 
        c = self.client
        logged_in = c.login(username= 'test', password= 'password')
        assert logged_in
    
        # check we can get a notebook via its guid
        response = c.get('/notebook/%s/' % nb.guid)
        assert response.status_code == 200
    
        # and that non existant notebooks raise 404
        # currently raises TemplateDoesNotExist
        # response = c.get('/notebook/doesnotexist/')
        # assert response.status_code == 404
        # nb.delete() #clean up
    
    
