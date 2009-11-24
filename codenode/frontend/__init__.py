# These are package level test setups that run before and after all frontend testing.
# Importing is done inside the function to prevent anything funny happening when importing this
# file.

def setUpPackage(self):    
    # create a search index
    from codenode.frontend.search import search
    import tempfile
    search.SEARCH_INDEX = tempfile.mktemp() # do not create the file, otherwise index is not created
    search.create_index()
    
def tearDownPackage():
    # delete search index
    from codenode.frontend.search import search
    import shutil
    shutil.rmtree(search.SEARCH_INDEX)