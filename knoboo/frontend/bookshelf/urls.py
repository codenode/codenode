from django.conf.urls.defaults import *

from frontend.bookshelf.views import bookshelf, folders
from frontend.bookshelf.views import load_bookshelf_data, change_notebook_location
from frontend.bookshelf.views import empty_trash, new_notebook

urlpatterns = patterns('',
    url(r'^$', bookshelf, name='bookshelf'),
    url(r'^load$', load_bookshelf_data, name='load_bookshelf_data'),
    url(r'^folders$', folders, name='folders'),
    url(r'^move$', change_notebook_location, name='change_notebook_location'),
    url(r'^new$', new_notebook, name='new_notebook'),
    url(r'^emptytrash$', empty_trash, name='empty_trash'),
)
