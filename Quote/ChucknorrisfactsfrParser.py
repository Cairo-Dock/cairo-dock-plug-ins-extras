# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class ChucknorrisfactsfrParser(SGMLParser):

  def reset(self):
    SGMLParser.reset(self)
    self.url = "http://www.chucknorrisfacts.fr/facts/alea"
    self.quote = []                                         # list of quotes to be filled
    self.inside_div_element = False                         # indicates if the parser is inside the <div></div> tag
    self.current_quote = ""

  def start_div(self, attrs):
    for name, value in attrs:
      if name == "class" and value == "factbody":           # <div class="factbody">...</div>
        self.inside_div_element = True
      if name == "class" and value == "vote":               # Inside the same <div> tag there is a subcontent "vote", which we have to discard
        self.end_div()

  def end_div(self):
    self.quote.append(self.current_quote)
    self.current_quote = ""
    self.inside_div_element = False

  def handle_data(self, text):
    if self.inside_div_element:                             # Concatenate all the content inside <div>...</div>
      self.current_quote += text

  def parse(self, page):
    self.feed(str(page))                                    # feed the parser with the page's html
    self.close() 
