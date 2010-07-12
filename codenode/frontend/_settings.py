import os
import sys
import commands

# To make the paths clearer I have moved them to the top of the file.
# There are two paths, the PROJECT_PATH is a link into the code and static assets
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_PATH, "."))

# The HOME_PATH (formally ENV_PATH) is a link to data, plots, search indexes, etc
HOME_PATH = os.path.join(os.path.abspath('.'), 'data')


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(HOME_PATH, 'codenode.db') # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
# XXX Uh, what about this?
SECRET_KEY = 'n1ty3bi2oa-@jed0k@@n6%c4&lhoc$c19a8+82&597sqz&x*8!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'codenode.frontend.urls'

#New user registration functionality:
ACCOUNT_ACTIVATION_DAYS = 3

#User personal settings functionality:
AUTH_PROFILE_MODULE = "usersettings.UserSettings"

###############################
#Search
SEARCH_INDEX = os.path.join(HOME_PATH, 'search_index')

APP_HOST = 'localhost'
APP_PORT = 8000

#Available types of notebooks: #XXX Clean up and do intelligent detection:
PLOT_IMAGES = os.path.join(HOME_PATH, 'plot_images')

COMPRESS = False
COMPRESS_VERSION = True
COMPRESS_CSS_FILTERS = None #('compress.filters.csstidy_python.CSSTidyFilter', ) 

COMPRESS_CSS = {
    'bookshelf': {
        'source_filenames': ('css/bookshelf.css', ),
        'output_filename': 'css/bookshelf_compressed.css',
    },
    'notebook': {
        'source_filenames': ('css/notebook.css', ),
        'output_filename': 'css/notebook_compressed.css',
    }
}

COMPRESS_JS = {
    'bookshelf': {
        'source_filenames': ('external/jquery.min.js', 'external/jquery-ui.min.js', 
                'external/jquery.color.js', 'external/jquery.dom.js', 
                'external/jquery.contextmenu.js', 'external/jqModal.dev.js',
                'external/splitter.js', 'js/bookshelf.js'),
        'output_filename': 'js/bookshelf_compressed.js',
    },

    'notebook': {
        'source_filenames': ('external/jquery.min.js', 'external/jquery.ifixpng.js', 
                'external/jquery.contextmenu.js', 'external/jquery.dom.js', 
                'js/BrowserDetect.js', 'js/Notebook.js', 'js/Indicator.js', 
                'js/Cell.js', 'js/Async.js', 'js/Delegator.js', 'js/DOM.js', 
                'js/SaveLoad.js', 'js/Spawner.js', 'js/TreeBranch.js', 'js/Completer.js', 
                'js/Util.js', 'external/json2.js', 'external/jquery.dimensions.js',
            'external/jquery.fieldselection.js', 'external/jqModal.dev.js'),
        'output_filename': 'js/notebook_compressed.js',
    }
}

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'codenode.frontend.registration',
    'codenode.frontend.bookshelf',
    'codenode.frontend.notebook',
    'codenode.frontend.backend',
    'codenode.frontend.usersettings',
    'compress',
    'codenode',
)


#########################################################
# This is run every time something imports settings...FIX
# Certain parts of the system might not want to import 
# this as some settings may be overridden by cmd options.
"""
_BANNERLEN = 70
try:
    from local_settings import *
    print "*"*_BANNERLEN
    print "*"
    print "* Open your web browser to http://%s:%s" % (APP_HOST, APP_PORT)
    print "*"
    print "*"*_BANNERLEN
except ImportError, exp:
    print "*"*_BANNERLEN
    print "*"
    print "! Warning: No 'local_settings.py' found, using defaults."
    print "! See '$codenode/local_settings.py.example'."
    print "*"
    print "-"*_BANNERLEN
    print "*"
    print "* Open your web browser to http://%s:%s" % (APP_HOST, APP_PORT)
    print "*"
    print "*"*_BANNERLEN
del _BANNERLEN

"""
