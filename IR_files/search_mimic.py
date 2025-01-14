#!/usr/bin/env python


import sys, os, lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.search import IndexSearcher

"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer):
    while True:
        print
        print("Hit enter with no input to quit.")
        command = input("Query:")
        if command == '':
            return

        print
        print("Searching for:", command)
        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print("%s total matching documents." % len(scoreDocs))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print('note_id:', doc.get("note_id"), 'chartdate:', doc.get("chartdate"))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Lucene index folder path is required. For example:")
        print("python search_mimic.py mimiciii.Index")
        sys.exit(1)

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)

    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = FSDirectory.open(Paths.get(sys.argv[1]))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run(searcher, analyzer)
    directory.close()
    del searcher
