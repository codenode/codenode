"""Backend Kernel Server related settings

These settings are entirely independent of the frontend/django app server.

The backend may eventually support a django powered admin web interface.
"""
import os
import commands
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

#Interface to listen on
KERNEL_HOST = 'localhost'
KERNEL_PORT = 8337

TWISTD = "twistd"
NOTEBOOK_TYPES = ["python", "sage"]
PYTHON_BINARY = commands.getoutput("/usr/bin/which python")
SAGE_BINARY = "/Applications/sage/sage"

ENGINES_PATH = os.path.join(os.path.abspath('.'), 'data')

try:
    from local_settings import *
except ImportError, exp:
    pass

