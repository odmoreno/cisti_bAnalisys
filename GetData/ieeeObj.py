
# Definir la clase para el objeto ieee

class PaperInfo:
    def __init__(self, idpaper, title, authors, authAff, pubYear, abstract, issn, isbns, doi,
                 pdflink, authorKeywork, ieeeTerms, refCount, citationCount, publisher):
        self.title = title
        self.id = idpaper
        self.authors = authors
        self.authAff = authAff
        self.pubYear = pubYear
        self.abstract = abstract
        self.issn = issn
        self.isbns = isbns
        self.doi = doi
        self.pdflink = pdflink
        self.authorKeywork = authorKeywork
        self.ieeeTerms = ieeeTerms
        self.refCount = refCount
        self.artCitationCount = citationCount
        self.publisher = publisher

    def set_new_authors(self, newAuthors):
        self.newAuthors = newAuthors
    def to_dict(self):
        return {
            'title': self.title,
            'doi': self.doi,
            'authors': self.authors,
            'authAff': self.authAff,
            'year': self.pubYear,
            'abstract': self.abstract,
            'pdflink': self.pdflink,
            'authorKeywords': self.authorKeywork,
            'ieeeTerms': self.ieeeTerms,
            'refCount': self.refCount,
            'artCitationCount': self.artCitationCount,
            'publisher': self.publisher
        }

    def dict_min(self):
        return {
            'id': self.id,
            'doi': self.doi,
            'title': self.title,
            'year': self.pubYear,
            'pdflink': self.pdflink,
            'authors': self.newAuthors,
        }

    def __repr__(self):
        return f"PaperInfo(title={self.title}, authors={self.authors}, authAff={self.authAff}, pubYear={self.pubYear},abstract={self.abstract}, issn={self.issn}, isbns={self.isbns}, doi={self.doi}, pdflink={self.pdflink},authorKeywork={self.authorKeywork}, ieeeTerms={self.ieeeTerms}, refCount={self.refCount}, artCitationCount={self.artCitationCount}, publisher={self.publisher})"
    
