# This is a part of the external Moon applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from sgmllib import SGMLParser

class MoonCalendarParser(SGMLParser):

    def reset(self):                              
        SGMLParser.reset(self)
        self.url = "http://www.briancasey.org/artifacts/astro/moon.cgi"
        self.information = ""
        self.moon_image = ""
        self.inside_td_element = False                                              # indica se o parser esta dentro de <td></td> tag
        self.stop_parsing = False                                                   # identifies the end of the useful data

    def start_img(self, attrs):
        self.moon_image = (dict(attrs)["src"]).split('/')[-1]                       # /image/moon06b.gif => moon06b.gif

    def start_td(self, attrs):
        for name, value in attrs:
            if name == "width" and value == "225":                                  # the useful information is all before this td
                self.stop_parsing = True                                            # i was lucky that there is this google ad td which
        self.inside_td_element = True                                               # that could be the referential to the end of the parsing

    def end_td(self):
        self.inside_td_element = False

    def handle_data(self, text):
        if not self.stop_parsing:
            if self.inside_td_element:
                # self.information.append(text)
                self.information += text

    def parse(self, page):
        self.feed(str(page))                                                             # feed the parser with the page's html
        self.close()
