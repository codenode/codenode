import os 

from _settings import *

# Destop codende has a home directory by default, or picks it up from the CODENODE_HOME directory
HOME_PATH = os.environ.get('CODENODE_HOME',
    os.path.join(os.path.expanduser("~"), '.codenode') 
)

DATABASE_ENGINE = 'sqlite3'          
DATABASE_NAME = os.path.join(HOME_PATH, 'codenode.db') # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


SEARCH_INDEX = os.path.join(HOME_PATH, 'search_index')

PLOT_IMAGES = os.path.join(HOME_PATH, 'plot_images')
