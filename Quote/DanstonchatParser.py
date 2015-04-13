# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class DanstonchatParser(SGMLParser):

  def reset(self):                              
    SGMLParser.reset(self)
    self.name = "Danstonchat.com"
    self.url = "http://danstonchat.com/random.html"
    self.quote = []
    self.inside_p_element = False                                            # indicates that the parser is currently processing the content inside <p></p> tag
    self.inside_p_a_element = False
    self.current_quote = ""

  def start_p(self, attrs):
    for name, value in attrs:
	    if name == "class" and value == "item-content":
		    self.inside_p_element = True
	
  def end_p(self):
    self.inside_p_a_element = False
    self.inside_p_element = False

  def start_a(self, attrs):
    if self.inside_p_element:
      self.inside_p_a_element = True
  
  def end_a(self):
    if self.inside_p_a_element:
      self.quote.append(self.current_quote)                                   # append the whole content found inside <p><a>...</a></p>,
      self.current_quote = ""                                                 # clear it for the next quote,
      self.inside_p_a_element = False 

  def handle_data(self, text):
    if self.inside_p_a_element:                                               # we are inside the <p><a>...</a></p> tag
      self.current_quote += text                                              # concatenas everything inside the tag tag

  def parse(self, page):
    self.feed(str(page))                                                      # feed the parser with the page's html
    self.close()
