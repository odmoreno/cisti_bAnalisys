
'''
Uso de APIs
https://github.com/danielnsilva/semanticscholar
https://github.com/fabiobatalha/crossrefapi

@Venue
'ACM Conference on Learning @ Scale'
'International Conference on Learning Analytics and Knowledge'
'''

import pyalex
pyalex.config.email = "oscarpol95@gmail.com"
#from pyalex import Works, Authors, Sources, Institutions, Concepts, Publishers, Funders

from semanticscholar import SemanticScholar

from crossref.restful import Works
from crossref.restful import Journals

from common_functions import *

crosssearch_fields = ['title', 'publisher-location', 'reference-count', 'publisher', 'event', 'short-container-title','funder', 'DOI', 'type', 'prefix', 'author',  'published', 'reference']

semantic_fields = ['citationCount', 'referenceCount', 'paperId', 'publicationTypes', 'publicationVenue', 'title', 'venue', 'year', 'references', 'abstract']

pyalex_fields = ['title', 'authorships', 'source', 'topics', 'type', 'type_crossref', 'publication_year', 'publication_date']

def search_paper(doi, _getrefs = False):
    sch = SemanticScholar()
    data = {}
    refs = 'references'
    try:
        paper = sch.get_paper(doi)
        for value in paper.SEARCH_FIELDS:
          if value is not None:
            data[value] = paper[value]
        if _getrefs:
            refs = paper['references']
            data['references'] = refs
        data['found'] = True
    except Exception as e:
        print(e)
        print(f"Paper with DOI {doi} not found. {e}")
        data['found'] = False
    return data

def search_papers_sch(doi):
    sch = SemanticScholar()
    data = {}
    try:
        paper = sch.get_paper(doi)
        for value in semantic_fields:
          if value is not None:
            data[value] = paper[value]
        refs = paper['references']
        data['references'] = refs
        data['found'] = True
    except Exception as e:
        print(e)
        print(f"Paper with DOI {doi} not found. {e}")
        data['found'] = False
    return data

def search_in_crossref(doi):
    works = Works()
    data = {}
    try:
        paper = works.doi(doi)
        for value in crosssearch_fields:
            if value in paper:
                data[value] = paper[value]
        data['found'] = True
    except Exception as e:
        print(f"Paper with DOI {doi} not found. {e}")\

    return data

def search_in_pyalex(doi):
    linkdoi = 'https://doi.org/' + doi
    data = {}
    try:
        paper = pyalex.Works()[linkdoi]
        for value in pyalex_fields:
            if value in paper:
                data[value] = paper[value]
        data['found'] = True
    except Exception as e:
        print(f"Paper with DOI {doi} not found. {e}")
    return data


def search_paper_doi(id):
    sch = SemanticScholar()
    doi = ''
    refs = 'references'
    try:
        paper = sch.get_paper(id)
        doi = paper['externalIds']['DOI']
    except Exception as e:
        fail_message(e)
        print(f"Paper with ID {id} not found. {e}")
    return doi

def get_paper_refs(doi):
    sch = SemanticScholar()
    data = {}
    try:
        paper = sch.get_paper(doi)
        refs = paper['references']
        data['references'] = refs
    except Exception as e:
        print(e)
        print(f"Paper with DOI {doi} not found. {e}")
        data['found'] = False
    return data

def search_paper_ref(doi):
    sch = SemanticScholar()
    data = {}
    values = ["publicationVenue", "venue", "year", "referenceCount", "citationCount"]
    try:
        paper = sch.get_paper(doi)
        for value in values:
            if value is not None:
                data[value] = paper[value]
        data['found'] = True
    except Exception as e:
        print(e)
        print(f"Paper with DOI {doi} not found. {e}")
        data['found'] = False

    return data

def search_authors(doi):
    works = Works()
    field = 'author'
    autores = []
    try:
        paper = works.doi(doi)
        if field in paper:
            autores = paper[field]
    except Exception as e:
        print(f"Paper with DOI {doi} not found. {e}")
    return autores

#'WorldCIST'
#'World Conf Inf Syst Technol'
#'World Conference on Information Systems and Technologies'
def test_sscholar():
    sch = SemanticScholar()
    paper = sch.get_paper('10.1007/978-3-031-04826-5_1')
    papers = sch.get_papers(['bb15f3727f827a3cb88b5d3ca48415c09b40a88f'])
    paper = sch.get_paper('10.18608/jla.2020.73')
    author = sch.get_author('2972227')
    aa = sch.search_author('Alan M. Turing')
    a1 = sch.search_author('Yankun Zhao')
    a2 = sch.search_author('Mehmet Hamza Erol')
    a3 = sch.search_author('Jihyeong Hong')
    a4 = sch.search_author('Juho Kim')
    #paper = sch.get_paper('10.18608/jla.2023.7775')
    for field in paper.SEARCH_FIELDS:
        print(f'Field {field} : {paper[field]}.')
    print(' ----------- ')
    for author in paper.authors:
        print(f'AuthorID: {author.authorId} , AuthorName: {author.name}')
        results = sch.get_author(author.authorId)
        print(f'Affiliations: {results.affiliations}')
        print(f'Citation Counts: {results.citationCount}')
        print(f'Paper Count: {results.paperCount}')
        print('-->')
        for paper in results.papers:
            print(f'Paper: {paper.title}, {paper.year}')
    #results = sch.search_paper(' ', venue=['Journal of Learning Analytics'])
    #print(len(results))
    #for result in results:
    #    print(result)

def test_crossref():
    works = Works()
    paper = works.doi('10.1145/2090116.2090117')
    paper2 = works.doi('10.18608/jla.2023.7775')
    paper = works.doi('10.1007/978-3-031-04826-5_1')
    print(paper)
    autores = paper['author']
    for autor in autores:
        name = autor['given'] +' '+autor['family']
        w1 = works.query(author=name)
        #for item in w1:
        #    print(f"Title: {item} ")
    #w1 = works.query(event_acronym='LAK').sort('relevance')
    w1 = works.query(publisher_name='Society for Learning Analytics Research') #works.query(event_acronym='LAK', publisher_name='ACM').sort('published').order('asc')
    print(works.query(event_acronym='LAK', publisher_name='ACM').count())
    print(works.query(publisher_name='Society for Learning Analytics Research').count())
    #w1 = works.query(publisher_name='Society for Learning Analytics Research').sort('relevance')
    for item in w1:
        print(f"Title: {item['title'][0]} , Year: {item['published']},  Event: {item['event']['acronym']}")

def search_journals():
    #journals = Journals().query('Learning Analytics')
    journals = Journals().query('WorldCIST')
    print(journals)
    for journal in journals:
        print(f"Journal : {journal['title']}")
        print(f"Publisher : {journal['publisher']}")
        print(f"Counts : {journal['counts']}")
        print('-------')


def get_countries_dict():
    path = 'data/countries.json'
    paises = load_generic(path)

    country_dict = {item["country"].lower(): item for item in paises}
    save_generic( 'data/paises.json', country_dict)

def pyalex_test(_doi = '10.23919/CISTI.2017.7975672'):
    linkdoi = 'https://doi.org/' + _doi
    #https://link.springer.com/chapter/10.1007/978-3-031-04826-5_1
    paperPyAlex = pyalex.Works()[linkdoi]
    print(paperPyAlex)
    works = Works()
    paperCrossRef = works.doi(_doi)
    print(paperCrossRef)
    sch = SemanticScholar()
    paperSch = sch.get_paper(_doi)
    print(paperSch)
    #paper3 = sch.get_paper('10.1016/j.asoc.2021.107561')
    print(f'Fin')

if __name__ == '__main__':
    # test_sscholar()
    # test_crossref()
    # search_journals()
    # get_countries_dict()
    pyalex_test()
    pass