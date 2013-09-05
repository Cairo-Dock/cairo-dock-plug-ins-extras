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
        self.inside_nickname = False                                                # <p>"<nickname>phrase"</p>
        self.current_quote = ""

    def start_p(self, attrs):
        for name, value in attrs:
            if name == "class" and value == "qt":                                   # <p class="qt">...</p>
                self.inside_p_element = True
    
    def end_p(self):
        if self.inside_p_element:
            self.quote.append(self.current_quote)                                   # adiciona o conteudo completo da tag
            self.current_quote = ""                                                 # reinicia o armazenador do conteudo
            self.inside_p_element = False

    def handle_data(self, text):
        if self.inside_p_element:                                                   # estamos dentro de <p>...</p>
            self.current_quote += text
#            if not self.inside_nickname:                                            # <nickname> quote
#                if text == '<':                                                     # entered the "nickname area"
#                    self.inside_nickname = True
#                    self.current_quote += '\n<'                                     # linebreak
#                else:
#                    self.current_quote += text                                      # concatena tudo que tiver dentro da tag
#            else:                                                                   
#                self.current_quote += text                                          # concatenate all the nickname
#                if text == '>':                                                     # nickname is over
#                    self.inside_nickname = False                                    # set it

    def parse(self, page):
        self.feed(str(page).encode('utf8'))                                                             # feed the parser with the page's html
        self.close()
