# This is a part of the external Google applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class GoogleParser(SGMLParser):

    def reset(self):                              
        SGMLParser.reset(self)
        self.url = "http://www.google.com/search?q="
        self.inside_h3_element = False                                              # indica se o parser esta dentro de <h3></h3> tag
        self.inside_h3_a_element = False                                            # indica se o parser esta dentro de <h3><a></a></h3> tag
        self.urls = []
        self.descriptions = []
        self.current_description_piece = ""

    def start_h3(self, attrs):
        for name, value in attrs:
            if name == "class" and value == "r":                                    # <h3 class="r">...</h3>
                self.inside_h3_element = True
    
    def end_h3(self):
        self.inside_h3_element = False
        while len(self.urls) > len(self.descriptions) + 1:                            # url are added before the description: add 'no description' if some of them are missing
            self.descriptions.append(_("No description"))
        if len(self.urls) > len(self.descriptions) or self.current_description_piece: # add a description only if there is a url which doesn't have a description and if this description is not empty
            self.descriptions.append(self.current_description_piece)                  # adiciona o conteudo completo da tag
            self.current_description_piece = ""                                       # reinicia o armazenador do conteudo

    def start_a(self, attrs):
        if self.inside_h3_element:
            self.inside_h3_a_element = True                                         # <h3 class="r"><a>...</a></h3>
            for name, value in attrs:
                if name == "href":
                    if value[0:7] == '/url?q=':                                     # we have a link formatted by Google: '/url?q=http://(...)&sa=(...)'
                        value = value[7:value.find('&')]                            # remove all chars after the first '&': &sa=(...)
                        value = value.replace("%3F","?").replace("%3D","=").replace("%26","&").replace("%3A",":")   # unescape some XML chars
                    elif value[0] == '/':                                           # we have a link to another Google tool: e.g. images
                        value = 'http://www.google.com' + value
                    self.urls.append(value)

    def end_a(self):
        if self.inside_h3_element:
            self.inside_h3_a_element = False

    def handle_data(self, text):
        if self.inside_h3_a_element:                                                # estamos dentro de <h3 class="r"><a>...</a></h3>
            self.current_description_piece += text                                  # concatena tudo que tiver dentro da tag

    def parse(self, page):
        self.feed(str(page))                                                             # feed the parser with the page's html
        self.close()
