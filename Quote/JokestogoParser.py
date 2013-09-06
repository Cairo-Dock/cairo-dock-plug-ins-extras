# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class JokestogoParser(SGMLParser):

    def reset(self):                              
        SGMLParser.reset(self)
        self.name = "Jokes2go.com"
        self.url = "http://www.jokes2go.com/cgi-perl/randjoke.cgi?type=j"
        self.quote = []
        self.inside_pre_element = False                                             # indica se o parser esta dentro de <pre></pre> tag
        self.current_quote = ""

    def start_pre(self, attrs):
       self.inside_pre_element = True
    
    def end_pre(self):
        self.inside_pre_element = False
        self.quote.append(self.current_quote)
        self.current_quote = ""

    def handle_data(self, text):
        if self.inside_pre_element:                                                 # estamos dentro de <pre>...</pre>
            self.current_quote += text

    def parse(self, page):
        self.feed(str(page))                                                             # feed the parser with the page's html
        self.close() 
