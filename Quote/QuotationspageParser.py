# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class QuotationspageParser(SGMLParser):

    def reset(self):
        SGMLParser.reset(self)
        self.name = "Quotationspage.com"
        self.url = "http://www.quotationspage.com/qotd.html"
        self.quote = []
        self.author = []
        self.inside_dt_a_element = False                                            # indica se o parser esta dentro de <dt><a></a></dt> tag
        self.inside_dt_element = False                                              # indica se o parser esta dentro de <dt></dt> tag

        self.inside_dd_element = False                                              # indica se o parser esta dentro de <dd></dd> tag
        self.inside_dd_b_element = False                                            # indica se o parser esta dentro de <dt><b><b></dt> tag
        self.inside_dd_b_a_element = False                                          # indica se o parser esta dentro de <dt><b><a><a><b></dt> tag

    def start_dt(self, attrs):
        for name, value in attrs:
            if name == "class" and value == "quote":                                # <dt class="quote">...</dt>
                self.inside_dt_element = True
    
    def end_dt(self):
        self.inside_dt_element = False

    def start_dd(self, attrs):
        for name, value in attrs:
            if name == "class" and value == "author":                               # <dd class="author">...</dd>
                self.inside_dd_element = True

    def end_dd(self):
        self.inside_dd_element = False

    def start_b(self, attrs):
        if self.inside_dd_element:
            self.inside_dd_b_element = True

    def end_b(self):
        self.inside_dd_b_element = False

    def start_a(self, attrs):
        if self.inside_dt_element:
            self.inside_dt_a_element = True                                        # <dt class="quote"><a>Quote</a></dt>
        if self.inside_dd_b_element:
            self.inside_dd_b_a_element = True                                      # <dd class="author"><b><a>Quote</a></b></dd>

    def end_a(self):
        self.inside_dt_a_element = False
        self.inside_dd_b_a_element = False

    def handle_data(self, text):
        if self.inside_dt_a_element:                                                # estamos dentro de <dt><a>...</a></dt>
            self.quote.append(text)
        if self.inside_dd_b_a_element:                                              # estamos dentro de <dd><b><a>...</a></b></dd>
            self.author.append(text)        

    def parse(self, page):
        self.feed(page)                                                             # feed the parser with the page's html
        self.close() 
