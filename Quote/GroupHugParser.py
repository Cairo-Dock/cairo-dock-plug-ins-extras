# This is a part of the external Quote applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class GroupHugParser(SGMLParser):

	def reset(self):
		SGMLParser.reset(self)
		self.url = "http://grouphug.us/random"
		self.quote = []
		self.author = []
		self.inside_div_element = False											  	# indica dentro da <div class="content"></div> tag
		self.inside_div_p_element = False											# indica dentro da <div class="content"><p></p></div> tag
		self.current_quote = ""

	def start_div(self, attrs):
		for name, value in attrs:
			if name == "class" and value == "content":						   	 	# <dt class="content">...</dt>
				self.inside_div_element = True

	def end_div(self):
		if self.inside_div_element:
			self.quote.append(self.current_quote)
			self.current_quote = ""												 	# reinicia o armazenador do conteudo
			self.inside_div_element = False

	def start_p(self, attrs):
		if self.inside_div_element:
			self.inside_div_p_element = True

	def end_p(self):
		# if self.inside_div_element:
		self.inside_div_p_element = False
											   										# adiciona o conteudo completo da tag
	def handle_data(self, text):
		if self.inside_div_p_element:												# estamos dentro de <div><p>...</p></div>
			self.current_quote += text

	def parse(self, page):
		self.feed(page)															 	# feed the parser with the page's html
		self.close() 
