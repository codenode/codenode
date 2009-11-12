import uuid

from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from django.utils import simplejson as json

from codenode.frontend.notebook import models
from codenode.frontend.search import views
from codenode.frontend.search import search

#If you see this error: 
#  OSError: [Errno 17] File exists: 'tests/search_index/_MAIN_LOCK'
#Do this:
#  First fix any errors, then do "rm -rf tests/search_index", then test again.
#See here:
#  http://groups.google.com/group/whoosh/browse_thread/thread/50a06857db36e792/dcbd7c4e2a4c842b


# this stores fixture data
f = {}


class TestSearch(TestCase):

    def setup(self):
        f['user1'] = User.objects.get(username__exact='test')
        f['user2'] = User.objects.get(username__exact='test2')

    def teardown(self):
        f = {}
        allnotebooks = models.Notebook.objects.all()
        for nb in allnotebooks:
            nb.delete()
        allcells = models.Cell.objects.all()
        for cell in allcells:
            cell.delete()

    def test_search(self):
        #XXX Turn off Nose doctests?
        #"""
        #Add 2 Cells into 2 different Notebooks, 
        #one with correct search terms, 
        #and the other without, test that
        #only the Notebook with the correct search
        #terms appears in the results.
        #"""
        nb1 = models.Notebook(owner=f['user1'])
        nb1.save()
        nb2 = models.Notebook(owner=f['user1'])
        nb2.save()
 
        cell1 = models.Cell(
            guid=str(uuid.uuid4()).replace("-", ""), 
            notebook=nb1,
            owner=nb1.owner,
            content="foo=1\nbar=foo+foo"
            )
        cell1.save()
 
        cell2 = models.Cell(
            guid=str(uuid.uuid4()).replace("-", ""), 
            notebook=nb2,
            owner=nb2.owner,
            content="baz=1\nbar=baz+baz"
            )
        cell2.save()

        guids = [result["nbid"] for result in search.search("foo")]
        assert nb1.guid in guids
        assert nb2.guid not in guids


    def test_view_search(self):
        nb1 = models.Notebook(owner=f['user1'])
        nb1.save()
        nb2 = models.Notebook(owner=f['user2'], title="Foo is Foo")
        nb2.save()
        nb3 = models.Notebook(owner=f['user2'])
        nb3.save()
 
        cell1 = models.Cell(
            guid=str(uuid.uuid4()).replace("-", ""), 
            notebook=nb1,
            owner=nb1.owner,
            content="foo=1\nbar=foo+foo"
            )
        cell1.save()
 
        cell2 = models.Cell(
            guid=str(uuid.uuid4()).replace("-", ""), 
            notebook=nb2,
            owner=nb2.owner,
            content="foo=1\nbar=foo+foo"
            )
        cell2.save()

        cell3 = models.Cell(
            guid=str(uuid.uuid4()).replace("-", ""), 
            notebook=nb3,
            owner=nb3.owner,
            content="baz=1\nfump=baz+baz"
            )
        cell3.save()

        c = Client()
        logged_in = c.login(username='test2', password='password')
        assert logged_in
        response = c.get('/search', {'q':'foo'})
        resp = json.loads(response.content)
        assert resp["query"] == "foo"
        result_nbid = resp["results"][0][0]
        result_title = resp["results"][0][1]
        assert nb2.title == result_title
        assert nb1.guid != result_nbid #incorrect notebook owner 
        assert nb2.guid == result_nbid #contains search term
        assert nb3.guid != result_nbid  #no search terms
