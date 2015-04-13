# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class XkcdbParser(SGMLParser):

  def reset(self):                              
    SGMLParser.reset(self)
    self.name = "Xkcdb.com"
    self.url = "http://www.xkcdb.com/?random"
    self.quote = []
    self.inside_span_element = False                                          # indicates that the parser is within the <span></span> tag
    self.current_quote = ""

  def start_span(self, attrs):
    for name, value in attrs:
      if name == "class" and value == "quote":                                # <span class="quote">...</p>
        self.inside_span_element = True
  
  def end_span(self):
    self.inside_span_element = False
    self.quote.append(self.current_quote)                                     # concatenates all the contents inside the tag
    self.current_quote = ""                                                   # restart the container

  def handle_data(self, text):
    if self.inside_span_element:                                              # we are inside the  <span>...</span>
      text = text.replace('<', '[')
      text = text.replace('>', ']')
      self.current_quote += text                                              # concatenates all the content inside the tag

  def parse(self, page):
    self.feed(str(page))                                                      # feed the parser with the page's html
    self.close() 
