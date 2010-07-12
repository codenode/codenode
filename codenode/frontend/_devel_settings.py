import os 

from codenode.frontend._settings import *

HOME_PATH = os.path.join(PROJECT_PATH, '..', '..', 'devel', 'env')

DATABASE_ENGINE = 'sqlite3'          
DATABASE_NAME = os.path.join(HOME_PATH, 'codenode.db') # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


SEARCH_INDEX = os.path.join(HOME_PATH, 'search_index')

PLOT_IMAGES = os.path.join(HOME_PATH, 'plot_images')

INSTALLED_APPS = INSTALLED_APPS + ('django_nose', 'django_extensions')

TEST_RUNNER = 'django_nose.run_tests'
