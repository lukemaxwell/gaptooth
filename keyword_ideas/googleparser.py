from bs4 import BeautifulSoup
from lxml import html as ht


class Parser():
    tags_to_strip = ['span', 'em', 'a', 'b', 'br', 'html', 'body', 'p']
    
    def parse(self, html):
        data = []
        doc = ht.document_fromstring(html)
        f = open('debug_google.html', 'w+')

        
        f.write(unicode(html).encode('utf-8'))
        f.close()
        # Attempt to parse 1
        results = doc.xpath('//li[@class="g"]//div[@class="rc" and not(@data-extra)] | //li[@class="g card-section"]//div[@class="rc" and not (@data-extra)]')
        #print 'parse results: %s' % len(results)
        estimated = self.get_estimated(doc)
        #print estimated 
        # Get links and ranks
        for result in results:
            link = self.get_link(result)
            if len(link) > 0:                   
                # Ignore image links that are mixed in with standard results
                if not link.startswith('/images?q='):
                    title = self.get_title(result)
                    snippet = self.get_snippet(result)
                    row = [link, title, snippet, estimated]
                    data.append(row)
        return data
        
    def get_link(self, html_result):
        link = ''.join(html_result.xpath('h3[@class="r"]/a/@href'))
        if link.startswith('/url?q='):
                        q = link.index('?q=')
                        sa = link.index('&sa=')
                        link = link[q+3:sa]
        return link
        
    def get_title(self, html_result):
       
        title =  html_result.xpath('h3[@class="r"]/a/text()')
        #get rid of the em tags or we miss the keyword from the title and snippet
        soup = BeautifulSoup("".join(title))
        for tag in self.tags_to_strip:
           for match in soup.findAll(tag):
               match.replaceWithChildren()
               
        title = soup.renderContents()
        #print title 
        return title
        
    def get_snippet(self, html_result):
        snippet = html_result.xpath('div[@class="s"]//span[@class="st"]/text()')
        soup = BeautifulSoup("".join(snippet))
        #remove the dates inserted into some snippets by google
        elements_to_remove = soup.findAll("span", {"class":"f"})
        for element in elements_to_remove:
           element.extract()
        for tag in self.tags_to_strip:
           for match in soup.findAll(tag):
               match.replaceWithChildren()
        snippet = soup.renderContents()
        return snippet
        
    def get_estimated(self, html_doc):
        try:
            estimated = "".join(html_doc.xpath('//div[@id="resultStats"]/text()'))
        except: 
            estimated = int(0)
            return estimated
        estimated = estimated.replace(',', '')
        estimated = estimated.replace('.', '')
        #Extract the integer number of estimated results
        #Sometimes page numbers are included, so we always take the last integer from the string
        try:    
            ints = [int(s) for s in estimated.split() if s.isdigit()]
            estimated = ints[len(ints)-1]
        except IndexError:
            estimated = 0
        estimated = int(estimated)
        return estimated
