# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class VidademerdaParser(SGMLParser):

    def reset(self):
        SGMLParser.reset(self)
        self.url = "http://vidademerda.com.br/aleatorias"
        self.quote = []
        self.author = []
        self.inside_div_element = False                                              # indica se o parser esta dentro de <div></div> tag
        self.inside_div_p_element = False
        self.inside_b_element = False

    def start_div(self, attrs):
        for name, value in attrs:
            if name == "class" and value == "vdmContent":                            # <dt class="vdmContent">...</dt>
                self.inside_div_element = True

    def end_div(self):
        self.inside_div_element = False

    def start_p(self, attrs):
        if self.inside_div_element:
            self.inside_div_p_element = True

    def end_p(self):
        self.inside_div_p_element = False

    def start_b(self, attrs):
        for name, value in attrs:
            if name == "class" and value == "ajustM6":                               # <dt class="ajustM6">...</dt>
                self.inside_b_element = True

    def end_b(self):
        self.inside_b_element = False

    def handle_data(self, text):
        if self.inside_div_p_element:                                                # estamos dentro de <div><p>...</p></div>
            self.quote.append(text)
        if self.inside_b_element:
            self.author.append(text)

    def parse(self, page):
        self.feed(page)                                                             # feed the parser with the page's html
        self.close() 
