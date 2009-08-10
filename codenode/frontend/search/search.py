import os
from whoosh import index
from whoosh import analysis
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.filedb.filestore import FileStorage

SEARCH_INDEX = "search_index"

SEARCH_SCHEMA = Schema(
    guid=ID(stored=True), 
    owner=ID(stored=True), 
    title=TEXT(field_boost=3), 
    content=TEXT(analyzer=analysis.FancyAnalyzer())
)

def create_index(search_index=SEARCH_INDEX, search_schema=SEARCH_SCHEMA):
    if not os.path.exists(search_index):
        os.mkdir(search_index)
        storage = FileStorage(search_index)
        storage.create_index(search_schema)

def insert(inst, search_index=SEARCH_INDEX, search_schema=SEARCH_SCHEMA):
    ix = index.open_dir(search_index)
    writer = ix.writer()
    writer.add_document(guid=inst.guid, owner=inst.owner, title=inst.title, content=inst.content)
    writer.commit()

def search(q, default_field="content", search_index=SEARCH_INDEX):
    ix = index.open_dir(search_index)
    searcher = ix.searcher()
    parser = QueryParser(default_field, schema=ix.schema)
    query = parser.parse(q)
    results = searcher.search(query)
    return results

def fa(content):
    fa = analysis.FancyAnalyzer()
    return  [t.text for t in fa(content)]

class Doc(object):
    def __init__(self, guid, owner, title, content):
        self.guid=guid
        self.owner=owner
        self.title=title
        self.content=content


if __name__ == "__main__":
    os.system("rm -rf search_index")
    create_index()
    c0 = u"""for i in range(10):
            print i*i
         """
    c1 = u"""def foo(x, y):
            return x + y
         """
    c2 = u"""bar = foo(10, 20)"""

    cls = [Doc(unicode(i), u"agc", u"untitled",c) for (i,c) in enumerate([c0, c1, c2])]

    for c in cls:
        print fa(c.content)
        insert(c)

    res = search("foo")
    print list(res)
