import os
import sys
import commands
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_PATH, "."))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = PROJECT_PATH+'/../data/codenode.db' # Or path to database file if using sqlite3.
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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/'

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
SEARCH_INDEX = PROJECT_PATH+'/../data/search_index'

APP_HOST = 'localhost'
APP_PORT = 8000

#Available types of notebooks: #XXX Clean up and do intelligent detection:
NOTEBOOK_TYPES = ["python", "sage"]
PYTHON_BINARY = commands.getoutput("/usr/bin/which python")
SAGE_BINARY = "/Applications/sage/sage"

KERNEL_SERVICE = 'codenode'
KERNEL_HOST = 'localhost'
KERNEL_PORT = 8337

ENV_PATH = os.path.join(os.path.abspath('.'), 'data') #XXX
ENGINES_PATH = os.path.join(os.path.abspath('.'), 'data')


COMPRESS = False
COMPRESS_VERSION = True
COMPRESS_CSS_FILTERS = None #('apps.compress.filters.csstidy_python.CSSTidyFilter', ) #MUST use 'apps.compress..."

COMPRESS_CSS = {
    'bookshelf': {
        'source_filenames': ('static/css/bookshelf.css', ),
        'output_filename': 'static/css/bookshelf_compressed.css',
    },
    'notebook': {
        'source_filenames': ('static/css/notebook.css', ),
        'output_filename': 'static/css/notebook_compressed.css',
    }
}

COMPRESS_JS = {
    'bookshelf': {
        'source_filenames': ('static/external/jquery.js', 'static/external/jquery-ui.min.js', 'static/external/jquery.color.js',
            'static/external/jquery.dom.js', 'static/external/jquery.contextmenu.js', 'static/external/jqModal.dev.js',
            'static/external/splitter.js', 'static/js/bookshelf.js'),
        'output_filename': 'static/js/bookshelf_compressed.js',
    },

    'notebook': {
        'source_filenames': ('static/external/jquery.js', 'static/external/jquery.ifixpng.js', 'static/external/jquery.contextmenu.js',
            'static/external/jquery.dom.js', 'static/js/BrowserDetect.js', 'static/js/Notebook.js',
            'static/js/Indicator.js', 'static/js/Cell.js', 'static/js/Async.js', 'static/js/Delegator.js',
            'static/js/DOM.js', 'static/js/SaveLoad.js', 'static/js/Spawner.js', 'static/js/TreeBranch.js',
            'static/js/Completer.js', 'static/js/Util.js', 'static/external/json2.js', 'static/external/jquery.dimensions.js',
            'static/external/jquery.fieldselection.js', 'static/external/jqModal.dev.js'),
        'output_filename': 'static/js/notebook_compressed.js',
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
    'codenode.frontend.usersettings',
    'compress',
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
