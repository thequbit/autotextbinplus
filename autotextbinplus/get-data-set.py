
import os
from subprocess import call
from barking_owl import Scraper
import datetime
import requests
#from yapot import convert_document
from unpdfer import Unpdfer

class DocGrabber(object):

    doc_count = 0

    def doc_callback(self, _data, document):
        #print ''
        #print document
        #print ''
        #print _data
        url = document['url']
        print "Downloading PDF ..."
        with open('doc.pdf','wb') as f:
            resp = requests.get(url, stream=True)
            for block in resp.iter_content(1024):
                if not block:
                    break
                f.write(block)
        print "PDF Downloaded."
        #success, pdf_text = convert_document(
        #    pdf_filename = 'file.pdf',
        #    delete_files = True,
        #    page_delineation = '\n',
        #    verbose = True,
        #    make_thumbs = False,
        #)
        #u = Unpdfer()
        #created, pdftext, pdfhash, success = u.unpdf(
        #    filename = 'doc.pdf',
        #    SCRUB = False,
        #    verbose = True,
        #)
        call(['pdftotext','doc.pdf','doc-{0}.txt'.format(self.doc_count)])
        #if success == False:
        #    raise Exception('invalid pdf')
        #with open('doc-{0}.txt'.format(self.do_count),'w') as f:
        #    f.write(pdftext)
        os.remove('doc.pdf')
        self.doc_count += 1

    def scrape(self, url, level=1):

        s = Scraper(DEBUG=True)

        s.set_url_data({
            'target_url': url,
            'doc_types': [
                'application/pdf',
            ],
            'title': '',
            'description': '',
            'max_link_level': level,
            'creation_datetime': str(datetime.datetime.now()),
            'allowed_domains': [ 
            ],
            'sleep_time': 0,
        })

        s.set_callbacks(
            found_doc_callback = self.doc_callback,
        )

        data = s.start()

        return data

if __name__ == '__main__':

    url = 'http://henrietta.org/index.php/2012-05-16-11-50-52/town-board/agendas-minutes/2015-agenda-minutes-1'
    #url = 'http://timduffy.me/'

    dg = DocGrabber()
    dg.scrape(url, level=1)
