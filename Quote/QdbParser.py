# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class QdbParser(SGMLParser):

  def reset(self):                              
    SGMLParser.reset(self)
    self.name = "Qdb.us"
    self.url = "http://www.qdb.us/random"
    self.quote = []
    self.inside_span_element = False                                            # indicates that the parser is currently processing the content inside <span></span> tag
    self.current_quote = ""

  def start_span(self, attrs):
    for name, value in attrs:
      if name == "class" and value == "qt":                                     # <span class="qt">...</span>
          self.inside_span_element = True
  
  def end_span(self):
    self.inside_span_element = False
    self.quote.append(self.current_quote)                                       # add the whole content to the container
    self.current_quote = ""                                                     # clear it for the next quote

  def handle_data(self, text):
    if self.inside_span_element:                                                # we are inside the <span>...</span> tag
      self.current_quote += text

  def parse(self, page):
    self.feed(str(page))                                                        # feed the parser with the page's html
    self.close()
