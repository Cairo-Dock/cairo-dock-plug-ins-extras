# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class BashParser(SGMLParser):

  def reset(self):                              
    SGMLParser.reset(self)
    self.url = "http://bash.org/?random"
    self.quote = []
    self.inside_p_element = False                                             # # indicates that the parser is currently processing the content inside <p></p> tag
    self.inside_nickname = False                                              # <p>"<nickname>phrase"</p>
    self.current_quote = ""

  def start_p(self, attrs):
    for name, value in attrs:
      if name == "class" and value == "qt":                                   # <p class="qt">...</p>
        self.inside_p_element = True
  
  def end_p(self):
    if self.inside_p_element:
      self.quote.append(self.current_quote)                                   # add the whole content to the container
      self.current_quote = ""                                                 # clear it for the next quote
      self.inside_p_element = False

  def handle_data(self, text):
    if self.inside_p_element:                                                 # we are inside the <p>...</p> tag
      self.current_quote += text

  def parse(self, page):
    self.feed(str(page))                                                      # feed the parser with the page's html
    self.close()
