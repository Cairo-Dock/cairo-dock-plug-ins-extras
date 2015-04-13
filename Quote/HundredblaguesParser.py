# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class HundredblaguesParser(SGMLParser):

  def reset(self):
    SGMLParser.reset(self)
    self.url = "http://www.100blagues.com/random"
    self.quote = []                                         # list of quotes to be filled
    self.inside_div_element = False                         # indicates if the parser is inside the <div class="left comment">...</div> tag
    self.inside_div_a_element = False                       # indicates if the parser is inside the <div class="left comment">...<a href>...</a>...</div> tag
    self.current_quote = ""

  def start_div(self, attrs):
    for name, value in attrs:
      if name == "class" and value == "left comment":       # <div class="left comment">...</div>
        self.inside_div_element = True

  def end_div(self):
    self.inside_div_element = False

  def start_a(self, attrs):
    if self.inside_div_element:
      self.inside_div_a_element = True
  
  def end_a(self):
    if self.inside_div_a_element:
      self.quote.append(self.current_quote)                 # append the whole content found inside <div><a>...</a></div>,
      self.current_quote = ""                               # clear it for the next quote,
      self.inside_div_a_element = False                     # and mark as finished tag    

  def handle_data(self, text):
    if self.inside_div_a_element:                           # Concatenate all the content inside <div><a>...</a></div>
      self.current_quote += text

  def parse(self, page):
    self.feed(str(page))                                    # feed the parser with the page's html
    self.close() 
