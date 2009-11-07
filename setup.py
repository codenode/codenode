import os
try:
    from setuptools import setup 
except ImportError:
    from distutils.core import setup

# The below is taken from django. Compile the list of packages available, 
# because distutils doesn't have  an easy way to do this.
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
for dirpath, dirnames, filenames in os.walk('codenode'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
packages.append("codenode.twisted.plugins")



package_data = {'codenode':[
    'data/codenode.db',
    'frontend/static/js/*.js',
    'frontend/static/external/*.js',
    'frontend/static/css/*.css',
    'frontend/static/img/*.png',
    'frontend/static/img/*.gif',
    'frontend/static/admin/css/*.css',
    'frontend/static/admin/img/admin/*.gif',
    'frontend/static/admin/js/*.js',
    'frontend/static/admin/js/admin/*.js',
    'frontend/templates/*.html',
    'frontend/templates/admin/*.html',
    'frontend/templates/compress/*.html',
    'frontend/templates/bookshelf/*.html',
    'frontend/templates/notebook/*.html',
    'frontend/templates/usersettings/*.html',
]}



setup(
    name='codenode',
    version='0.1',
    url='http://codenode.org',
    download_url='http://pypi.python.org/pypi/codenode',
    install_requires=['Twisted>=8.2.0', 'Django>=1.0.2-final', 'Whoosh>=0.2.5', 'Sphinx', 'simplejson'],
    packages=packages,
    package_data=package_data,
    scripts=["codenode/scripts/codenode-admin"],
    description='Interactive Programming Notebook for the Web Browser',
    author='Alex Clemesha & Dorian Raymer',
    author_email='codenode-devel@googlegroups.com',
    license='BSD',
    classifiers = ['Development Status :: 3 - Alpha'],
    setup_requires=['nose>=0.11']
)
