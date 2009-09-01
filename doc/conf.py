import sys
import os
sys.path.insert(0, os.path.abspath('../codenode/codenode'))
import codenode

#Sphinx extension modules
extensions = ['sphinx.ext.autodoc']

project="Codenode"
copyright="Codenode Group 2009"
language="en"

master_doc = "index"

version = codenode.__version__

unused_docs = ['README']

#HTML opts
html_logo="images/codenode_logo_small.png"
html_title="Codenode Documentation"
html_favicon = "images/codenode_favicon.ico"

html_copy_source = False

html_theme = "default"
html_theme_options = {
    "rightsidebar":"false",
    "relbarbgcolor":"#252525",
    "footerbgcolor":"#3B595F",
    "footertextcolor":"#CFCFCF",
    "sidebarbgcolor":"#F6FFEF",
    "sidebartextcolor":"#000",
    "sidebarlinkcolor":"#000",
    "relbarbgcolor":"#4C696F",
    "relbartextcolor":"#CFCFCF",
    "relbarlinkcolor":"#FF6E2F",
    "bgcolor":"#FFF"
}
