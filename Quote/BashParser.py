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
        self.inside_p_element = False                                               # indica se o parser esta dentro de <p></p> tag
        self.current_quote = ""

    def start_p(self, attrs):
        for name, value in attrs:
            if name == "class" and value == "qt":                                   # <p class="qt">...</p>
                self.inside_p_element = True
    
    def end_p(self):
        self.inside_p_element = False
        self.quote.append(self.current_quote)                                       # adiciona o conteudo completo da tag
        self.current_quote = ""                                                     # reinicia o armazenador do conteudo

    def handle_data(self, text):
        if self.inside_p_element:                                                   # estamos dentro de <p>...</p>
            text = text.replace('<', '[')                                           # se a string contem '<nome>', gera o erro na hora do ShowDialog
            text = text.replace('>', ']')                                           # pango_layout_set_markup_with_accel: Unknown tag 'nome'
            self.current_quote += text                                              # concatena tudo que tiver dentro da tag

    def parse(self, page):
        self.feed(page)                                                             # feed the parser with the page's html
        self.close()
