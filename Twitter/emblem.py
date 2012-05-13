#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module is based on the svg_mod by benjamin <benjamin@vidya>
# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

import os

# All the emblems here were made using Inkscape and are based on a xlink pointing to the default icon.
# See xlink:href="./icon"

class Emblem:
  def __init__(self):
    self.emblem = os.path.abspath(os.path.join(os.getcwd(), './emblem.svg'))
    self.counter = 0
    self.size_small, self.size_medium, self.size_large = range(3)
    self.size = self.size_medium

  def update(self, counter):
    self.counter = counter
    svg = open(self.emblem, 'w')
    svg.write(self.draw())
    svg.close()
    
  def set_size_small(self):
    self.size = self.size_small

  def set_size_medium(self):
    self.size = self.size_medium

  def set_size_large(self):
    self.size = self.size_large
        
  def draw(self):
    if self.size == self.size_small:
      return self.draw_small()
    elif self.size == self.size_medium:
      return self.draw_medium()
    else:
      return self.draw_large()

  def draw_small(self):
    emblem_string = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="120"
   height="120"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.2 r9819"
   sodipodi:docname="emblem_large.svg">
  <defs
     id="defs4">
    <linearGradient
       x1="68"
       y1="52"
       x2="68"
       y2="84"
       id="linearGradient3948"
       xlink:href="#linearGradient3942"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       id="linearGradient3942">
      <stop
         id="stop3944"
         style="stop-color:#ffffff;stop-opacity:1"
         offset="0" />
      <stop
         id="stop3946"
         style="stop-color:#ffffff;stop-opacity:0"
         offset="1" />
    </linearGradient>
  </defs>
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="2.8"
     inkscape:cx="53.032794"
     inkscape:cy="53.985929"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     fit-margin-top="0"
     fit-margin-left="0"
     fit-margin-right="0"
     fit-margin-bottom="0"
     inkscape:window-width="1280"
     inkscape:window-height="775"
     inkscape:window-x="0"
     inkscape:window-y="1"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Camada 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-294.28571,-203.79074)">
    <image
       y="203.79074"
       x="294.28571"
       id="image3066"
       xlink:href="./icon"
       height="120"
       width="120" />
    <g
       id="g3234"
       transform="matrix(1.0149338,0,0,1.1054171,321.04511,150.44756)">
      <path
         style="opacity:0.1;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3960"
         inkscape:connector-curvature="0"
         d="m 89.986349,69.238985 c -0.21488,-1.561093 -1.973583,-1.971086 -3.08095,-2.785965 0.452305,-1.002477 1.307299,-1.880744 1.442147,-2.982622 0.09844,-1.212445 -1.013508,-2.114893 -2.161243,-2.135756 -0.574938,-0.191984 -1.529962,-0.121132 -1.883184,-0.466436 0.105461,-1.303923 0.927598,-2.804937 -0.05258,-3.95302 -0.907896,-1.060888 -2.339545,-0.509432 -3.503632,-0.325674 -0.950635,0.504422 -0.81239,-0.565783 -0.973216,-1.2035 -0.130627,-1.071533 -0.401383,-2.422333 -1.652276,-2.666162 -1.269606,-0.351715 -2.257329,0.785416 -3.345553,1.248885 -0.564682,0.197811 -0.761585,-1.032508 -1.178359,-1.409042 -0.426005,-1.011804 -1.521655,-1.848863 -2.654045,-1.413094 -1.095119,0.436651 -1.63445,1.627605 -2.458205,2.425428 -0.973647,-0.65486 -1.72467,-1.7847 -2.91707,-1.99934 -1.243767,-0.181639 -2.134633,0.905175 -2.372989,2.019516 -0.345055,0.444832 -0.243497,1.842522 -1.003052,1.403006 -1.213096,-0.355405 -2.631658,-1.302577 -3.801916,-0.341572 -1.164288,0.944179 -0.641361,2.603822 -0.785903,3.912444 -1.186176,0.269467 -2.880347,-0.340038 -3.868298,0.741757 -1.026659,1.143887 -0.143349,2.597452 0.237559,3.813095 0.487992,0.76899 -0.891072,0.672735 -1.319748,1.016916 -1.098052,0.268634 -2.195073,1.121664 -2.064313,2.380723 0.249354,1.192288 1.335753,1.97237 1.99934,2.949845 -0.871859,0.915157 -2.269562,1.493314 -2.556533,2.818742 -0.186067,1.142981 0.709312,1.986005 1.663193,2.403037 0.374257,0.418594 1.762649,0.565214 1.196802,1.235928 -0.585967,1.153839 -1.765734,2.450576 -0.926208,3.768425 0.810341,1.207354 2.476744,0.956157 3.736472,1.311043 -0.08576,1.227497 -0.781478,2.521328 -0.229433,3.703695 0.526899,1.071756 1.844115,1.213477 2.87647,0.879241 0.560732,0.07218 1.729076,-0.722239 1.724808,0.155757 0.28962,1.207178 0.140911,2.908592 1.527846,3.422546 1.38487,0.596205 2.576146,-0.697698 3.773565,-1.225564 0.454783,0.276534 0.742145,1.177337 1.132089,1.695641 0.455828,1.285443 2.259105,1.820804 3.255585,0.80819 0.610876,-0.645848 1.17573,-1.360459 1.769908,-2.032116 1.070537,0.696774 1.92142,2.036743 3.310382,1.999339 1.284689,-0.0939 1.81764,-1.335721 2.151522,-2.404812 0.206115,-0.763429 0.45194,-1.441171 1.291319,-0.838121 1.079697,0.400421 2.40691,1.016712 3.407356,0.09643 1.036768,-1.007403 0.54752,-2.574581 0.688297,-3.867575 1.24572,-0.135375 2.670869,0.29881 3.736472,-0.524417 0.936001,-0.804307 0.694064,-2.129136 0.219537,-3.122161 -0.129526,-0.619425 -0.912001,-1.544893 0.15361,-1.604149 1.111548,-0.448238 2.718145,-0.69704 2.904459,-2.123887 0.293747,-1.438242 -1.158981,-2.317711 -1.863365,-3.381883 -0.0012,-0.497479 0.978512,-0.910082 1.354831,-1.374896 0.68176,-0.486375 1.154931,-1.160958 1.098503,-2.027866 z" />
      <path
         inkscape:connector-curvature="0"
         style="opacity:0.15;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3956"
         transform="matrix(0,1.048834,-1.048834,0,146.16452,5.4895435)"
         d="m 60.9375,54.59375 a 0.86264402,0.86264402 0 0 0 -0.71875,0.4375 L 58.5,57.875 55.625,56.25 a 0.86264402,0.86264402 0 0 0 -1.28125,0.59375 l -0.625,3.3125 -3.28125,-0.5625 a 0.86264402,0.86264402 0 0 0 -1,1 L 50,63.875 46.6875,64.5 a 0.86264402,0.86264402 0 0 0 -0.59375,1.28125 l 1.625,2.875 L 44.875,70.375 A 0.86264402,0.86264402 0 0 0 44.75,71.78125 L 47.25,73.9375 45.15625,76.5 A 0.86264402,0.86264402 0 0 0 45.5,77.875 l 3.15625,1.1875 -1.125,3.15625 a 0.86264402,0.86264402 0 0 0 0.8125,1.15625 l 3.3125,0.03125 0.0625,3.3125 a 0.86264402,0.86264402 0 0 0 1.15625,0.8125 L 56,86.4375 l 1.1875,3.125 a 0.86264402,0.86264402 0 0 0 1.34375,0.34375 l 2.59375,-2.125 2.1875,2.5625 a 0.86264402,0.86264402 0 0 0 1.40625,-0.125 l 1.6875,-2.875 2.9375,1.625 a 0.86264402,0.86264402 0 0 0 1.25,-0.59375 l 0.59375,-3.28125 3.3125,0.5625 a 0.86264402,0.86264402 0 0 0 1,-1 L 74.9375,81.34375 78.21875,80.75 A 0.86264402,0.86264402 0 0 0 78.8125,79.5 l -1.625,-2.9375 2.875,-1.6875 a 0.86264402,0.86264402 0 0 0 0.125,-1.40625 L 77.625,71.28125 79.75,68.6875 a 0.86264402,0.86264402 0 0 0 -0.34375,-1.34375 l -3.125,-1.1875 1.09375,-3.125 A 0.86264402,0.86264402 0 0 0 76.5625,61.875 L 73.25,61.8125 73.21875,58.5 A 0.86264402,0.86264402 0 0 0 72.0625,57.6875 l -3.15625,1.125 -1.1875,-3.15625 a 0.86264402,0.86264402 0 0 0 -1.375,-0.34375 l -2.5625,2.09375 -2.15625,-2.5 a 0.86264402,0.86264402 0 0 0 -0.6875,-0.3125 z" />
      <path
         inkscape:connector-curvature="0"
         style="opacity:0.3;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3950"
         transform="matrix(0,1.048834,-1.048834,0,146.16452,5.4895435)"
         d="m 74.641931,84.79994 -4.128425,-0.680449 -0.772592,4.112178 -3.646724,-2.051417 -2.132447,3.599941 -2.725174,-3.174954 -3.235096,2.653498 -1.474928,-3.915545 -3.947546,1.387004 -0.04678,-4.183864 -4.183864,-0.04678 1.387005,-3.947547 -3.915546,-1.474927 2.653499,-3.235097 -3.174955,-2.725173 3.599941,-2.132447 -2.051417,-3.646724 4.112178,-0.772592 -0.680448,-4.128426 4.128425,0.680449 0.772592,-4.112178 3.646724,2.051417 2.132447,-3.599941 2.725173,3.174954 3.235097,-2.653498 1.474927,3.915545 3.947547,-1.387004 0.04678,4.183864 4.183863,0.04678 -1.387004,3.947547 3.915545,1.474927 -2.653498,3.235097 3.174955,2.725173 -3.599942,2.132447 2.051418,3.646724 -4.112178,0.772592 z" />
      <path
         transform="matrix(0,1.048834,-1.048834,0,146.16452,4.4895435)"
         inkscape:connector-curvature="0"
         style="color:#000000;fill:#ff0000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3139"
         d="m 74.641931,84.79994 -4.128425,-0.680449 -0.772592,4.112178 -3.646724,-2.051417 -2.132447,3.599941 -2.725174,-3.174954 -3.235096,2.653498 -1.474928,-3.915545 -3.947546,1.387004 -0.04678,-4.183864 -4.183864,-0.04678 1.387005,-3.947547 -3.915546,-1.474927 2.653499,-3.235097 -3.174955,-2.725173 3.599941,-2.132447 -2.051417,-3.646724 4.112178,-0.772592 -0.680448,-4.128426 4.128425,0.680449 0.772592,-4.112178 3.646724,2.051417 2.132447,-3.599941 2.725173,3.174954 3.235097,-2.653498 1.474927,3.915545 3.947547,-1.387004 0.04678,4.183864 4.183863,0.04678 -1.387004,3.947547 3.915545,1.474927 -2.653498,3.235097 3.174955,2.725173 -3.599942,2.132447 2.051418,3.646724 -4.112178,0.772592 z" />
      <text
         xml:space="preserve"
         style="font-size:16px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;letter-spacing:-1.32000005px;writing-mode:lr-tb;text-anchor:start;opacity:0.15;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         x="59.530632"
         y="77.325226"
         id="text3856"
         sodipodi:linespacing="125%"
         transform="scale(0.9999961,1.0000039)">         <tspan
   sodipodi:role="line"
   id="tspan3858"
   x="59.530632"
   y="77.325226"
   style="font-size:16px;font-weight:bold;letter-spacing:-1.32000005px;fill:#000000;-inkscape-font-specification:Sans Bold">{0}</tspan>       </text>
      <path
         style="opacity:0;fill:#000000;stroke:none;display:inline"
         id="path3919"
         inkscape:connector-curvature="0"
         d="m 60,72 4,-4 4,4 8,-8 4,4 -12,12 -8,-8 z" />
      <path
         style="opacity:0.6;color:#000000;fill:url(#linearGradient3948);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3933"
         inkscape:connector-curvature="0"
         d="M 71.5625,52 68.71875,55.34375 65.3125,52.5625 63.78125,56.65625 59.625,55.1875 l 0,1 4.15625,1.46875 1.53125,-4.09375 3.40625,2.78125 L 71.5625,53 73.8125,56.78125 77.625,54.625 78.4375,58.9375 82.625,58.25 82.78125,57.21875 78.4375,57.9375 77.625,53.625 73.8125,55.78125 71.5625,52 z m -11.96875,7.59375 -4.40625,0.03125 0.34375,1 4.0625,-0.03125 0,-1 z m 22.625,2 -0.15625,0.96875 3.8125,0.71875 0.5,-0.90625 -4.15625,-0.78125 z m -25.875,2.3125 -3.78125,1.40625 0.625,0.78125 3.46875,-1.3125 -0.3125,-0.875 z m 28.3125,2.53125 -0.4375,0.75 3.09375,1.84375 L 88,68.4375 l -3.34375,-2 z M 54.875,69.125 52,71.5625 l 0.6875,0.40625 2.65625,-2.25 L 54.875,69.125 z m 30.25,2.75 -0.46875,0.40625 2.15625,2.625 0.625,-0.21875 -2.3125,-2.8125 z m -29.78125,2.6875 -1.71875,3.0625 0.5,0.09375 1.65625,-2.90625 -0.4375,-0.25 z m 28.3125,2.53125 -0.3125,0.125 1.125,3.15625 0.34375,0 -1.15625,-3.28125 z m -25.875,2.3125 -0.5625,3.375 L 57.375,82.75 57.9375,79.4375 57.78125,79.40625 z" />
      <text
         xml:space="preserve"
         style="font-size:12px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;opacity:0.3;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         x="60.261475"
         y="76.597481"
         id="text3074"
         sodipodi:linespacing="125%">         <tspan
   sodipodi:role="line"
   id="tspan3076"
   x="60.261475"
   y="76.597481"
   style="font-size:14px;fill:#000000">{0}</tspan>       </text>
      <text
         transform="scale(0.9999961,1.0000039)"
         sodipodi:linespacing="125%"
         id="text3852"
         y="78.053253"
         x="58.71452"
         style="font-size:18px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;letter-spacing:-1.32000005px;writing-mode:lr-tb;text-anchor:start;opacity:0.05;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         xml:space="preserve">         <tspan
   style="font-size:18px;font-weight:bold;letter-spacing:-2.47000003px;fill:#000000;-inkscape-font-specification:Sans Bold"
   y="78.053253"
   x="58.71452"
   id="tspan3854"
   sodipodi:role="line">{0}</tspan>       </text>
      <text
         sodipodi:linespacing="125%"
         id="text3070"
         y="76.097481"
         x="60.261475"
         style="font-size:12px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;fill:#ff0000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         xml:space="preserve">         <tspan
   style="font-size:14px;fill:#ffffff"
   y="76.097481"
   x="60.261475"
   id="tspan3072"
   sodipodi:role="line">{0}</tspan>       </text>
    </g>
  </g>
</svg>"""
    formated_counter = str('%02d' % self.counter)
    return emblem_string.format(formated_counter)     # replaces the '{0}' on the triple-quoted http://stackoverflow.com/questions/3877623/in-python-can-you-have-variables-within-triple-quotes-if-so-how
    
  def draw_medium(self):
    emblem_string = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="120"
   height="120"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.2 r9819"
   sodipodi:docname="emblem_medium.svg">
  <defs
     id="defs4">
    <linearGradient
       x1="68"
       y1="52"
       x2="68"
       y2="84"
       id="linearGradient3948"
       xlink:href="#linearGradient3942"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       id="linearGradient3942">
      <stop
         id="stop3944"
         style="stop-color:#ffffff;stop-opacity:1"
         offset="0" />
      <stop
         id="stop3946"
         style="stop-color:#ffffff;stop-opacity:0"
         offset="1" />
    </linearGradient>
  </defs>
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="2.8"
     inkscape:cx="53.032796"
     inkscape:cy="53.985929"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     fit-margin-top="0"
     fit-margin-left="0"
     fit-margin-right="0"
     fit-margin-bottom="0"
     inkscape:window-width="1280"
     inkscape:window-height="775"
     inkscape:window-x="0"
     inkscape:window-y="1"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Camada 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-294.28571,-203.79074)">
    <image
       y="203.79074"
       x="294.28571"
       id="image3066"
       xlink:href="./icon"
       height="120"
       width="120" />
    <g
       id="g3234"
       transform="matrix(1.7761342,0,0,1.93448,249.82895,111.58303)">
      <path
         style="opacity:0.1;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3960"
         inkscape:connector-curvature="0"
         d="m 89.986349,69.238985 c -0.21488,-1.561093 -1.973583,-1.971086 -3.08095,-2.785965 0.452305,-1.002477 1.307299,-1.880744 1.442147,-2.982622 0.09844,-1.212445 -1.013508,-2.114893 -2.161243,-2.135756 -0.574938,-0.191984 -1.529962,-0.121132 -1.883184,-0.466436 0.105461,-1.303923 0.927598,-2.804937 -0.05258,-3.95302 -0.907896,-1.060888 -2.339545,-0.509432 -3.503632,-0.325674 -0.950635,0.504422 -0.81239,-0.565783 -0.973216,-1.2035 -0.130627,-1.071533 -0.401383,-2.422333 -1.652276,-2.666162 -1.269606,-0.351715 -2.257329,0.785416 -3.345553,1.248885 -0.564682,0.197811 -0.761585,-1.032508 -1.178359,-1.409042 -0.426005,-1.011804 -1.521655,-1.848863 -2.654045,-1.413094 -1.095119,0.436651 -1.63445,1.627605 -2.458205,2.425428 -0.973647,-0.65486 -1.72467,-1.7847 -2.91707,-1.99934 -1.243767,-0.181639 -2.134633,0.905175 -2.372989,2.019516 -0.345055,0.444832 -0.243497,1.842522 -1.003052,1.403006 -1.213096,-0.355405 -2.631658,-1.302577 -3.801916,-0.341572 -1.164288,0.944179 -0.641361,2.603822 -0.785903,3.912444 -1.186176,0.269467 -2.880347,-0.340038 -3.868298,0.741757 -1.026659,1.143887 -0.143349,2.597452 0.237559,3.813095 0.487992,0.76899 -0.891072,0.672735 -1.319748,1.016916 -1.098052,0.268634 -2.195073,1.121664 -2.064313,2.380723 0.249354,1.192288 1.335753,1.97237 1.99934,2.949845 -0.871859,0.915157 -2.269562,1.493314 -2.556533,2.818742 -0.186067,1.142981 0.709312,1.986005 1.663193,2.403037 0.374257,0.418594 1.762649,0.565214 1.196802,1.235928 -0.585967,1.153839 -1.765734,2.450576 -0.926208,3.768425 0.810341,1.207354 2.476744,0.956157 3.736472,1.311043 -0.08576,1.227497 -0.781478,2.521328 -0.229433,3.703695 0.526899,1.071756 1.844115,1.213477 2.87647,0.879241 0.560732,0.07218 1.729076,-0.722239 1.724808,0.155757 0.28962,1.207178 0.140911,2.908592 1.527846,3.422546 1.38487,0.596205 2.576146,-0.697698 3.773565,-1.225564 0.454783,0.276534 0.742145,1.177337 1.132089,1.695641 0.455828,1.285443 2.259105,1.820804 3.255585,0.80819 0.610876,-0.645848 1.17573,-1.360459 1.769908,-2.032116 1.070537,0.696774 1.92142,2.036743 3.310382,1.999339 1.284689,-0.0939 1.81764,-1.335721 2.151522,-2.404812 0.206115,-0.763429 0.45194,-1.441171 1.291319,-0.838121 1.079697,0.400421 2.40691,1.016712 3.407356,0.09643 1.036768,-1.007403 0.54752,-2.574581 0.688297,-3.867575 1.24572,-0.135375 2.670869,0.29881 3.736472,-0.524417 0.936001,-0.804307 0.694064,-2.129136 0.219537,-3.122161 -0.129526,-0.619425 -0.912001,-1.544893 0.15361,-1.604149 1.111548,-0.448238 2.718145,-0.69704 2.904459,-2.123887 0.293747,-1.438242 -1.158981,-2.317711 -1.863365,-3.381883 -0.0012,-0.497479 0.978512,-0.910082 1.354831,-1.374896 0.68176,-0.486375 1.154931,-1.160958 1.098503,-2.027866 z" />
      <path
         inkscape:connector-curvature="0"
         style="opacity:0.15;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3956"
         transform="matrix(0,1.048834,-1.048834,0,146.16452,5.4895435)"
         d="m 60.9375,54.59375 a 0.86264402,0.86264402 0 0 0 -0.71875,0.4375 L 58.5,57.875 55.625,56.25 a 0.86264402,0.86264402 0 0 0 -1.28125,0.59375 l -0.625,3.3125 -3.28125,-0.5625 a 0.86264402,0.86264402 0 0 0 -1,1 L 50,63.875 46.6875,64.5 a 0.86264402,0.86264402 0 0 0 -0.59375,1.28125 l 1.625,2.875 L 44.875,70.375 A 0.86264402,0.86264402 0 0 0 44.75,71.78125 L 47.25,73.9375 45.15625,76.5 A 0.86264402,0.86264402 0 0 0 45.5,77.875 l 3.15625,1.1875 -1.125,3.15625 a 0.86264402,0.86264402 0 0 0 0.8125,1.15625 l 3.3125,0.03125 0.0625,3.3125 a 0.86264402,0.86264402 0 0 0 1.15625,0.8125 L 56,86.4375 l 1.1875,3.125 a 0.86264402,0.86264402 0 0 0 1.34375,0.34375 l 2.59375,-2.125 2.1875,2.5625 a 0.86264402,0.86264402 0 0 0 1.40625,-0.125 l 1.6875,-2.875 2.9375,1.625 a 0.86264402,0.86264402 0 0 0 1.25,-0.59375 l 0.59375,-3.28125 3.3125,0.5625 a 0.86264402,0.86264402 0 0 0 1,-1 L 74.9375,81.34375 78.21875,80.75 A 0.86264402,0.86264402 0 0 0 78.8125,79.5 l -1.625,-2.9375 2.875,-1.6875 a 0.86264402,0.86264402 0 0 0 0.125,-1.40625 L 77.625,71.28125 79.75,68.6875 a 0.86264402,0.86264402 0 0 0 -0.34375,-1.34375 l -3.125,-1.1875 1.09375,-3.125 A 0.86264402,0.86264402 0 0 0 76.5625,61.875 L 73.25,61.8125 73.21875,58.5 A 0.86264402,0.86264402 0 0 0 72.0625,57.6875 l -3.15625,1.125 -1.1875,-3.15625 a 0.86264402,0.86264402 0 0 0 -1.375,-0.34375 l -2.5625,2.09375 -2.15625,-2.5 a 0.86264402,0.86264402 0 0 0 -0.6875,-0.3125 z" />
      <path
         inkscape:connector-curvature="0"
         style="opacity:0.3;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3950"
         transform="matrix(0,1.048834,-1.048834,0,146.16452,5.4895435)"
         d="m 74.641931,84.79994 -4.128425,-0.680449 -0.772592,4.112178 -3.646724,-2.051417 -2.132447,3.599941 -2.725174,-3.174954 -3.235096,2.653498 -1.474928,-3.915545 -3.947546,1.387004 -0.04678,-4.183864 -4.183864,-0.04678 1.387005,-3.947547 -3.915546,-1.474927 2.653499,-3.235097 -3.174955,-2.725173 3.599941,-2.132447 -2.051417,-3.646724 4.112178,-0.772592 -0.680448,-4.128426 4.128425,0.680449 0.772592,-4.112178 3.646724,2.051417 2.132447,-3.599941 2.725173,3.174954 3.235097,-2.653498 1.474927,3.915545 3.947547,-1.387004 0.04678,4.183864 4.183863,0.04678 -1.387004,3.947547 3.915545,1.474927 -2.653498,3.235097 3.174955,2.725173 -3.599942,2.132447 2.051418,3.646724 -4.112178,0.772592 z" />
      <path
         transform="matrix(0,1.048834,-1.048834,0,146.16452,4.4895435)"
         inkscape:connector-curvature="0"
         style="color:#000000;fill:#ff0000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3139"
         d="m 74.641931,84.79994 -4.128425,-0.680449 -0.772592,4.112178 -3.646724,-2.051417 -2.132447,3.599941 -2.725174,-3.174954 -3.235096,2.653498 -1.474928,-3.915545 -3.947546,1.387004 -0.04678,-4.183864 -4.183864,-0.04678 1.387005,-3.947547 -3.915546,-1.474927 2.653499,-3.235097 -3.174955,-2.725173 3.599941,-2.132447 -2.051417,-3.646724 4.112178,-0.772592 -0.680448,-4.128426 4.128425,0.680449 0.772592,-4.112178 3.646724,2.051417 2.132447,-3.599941 2.725173,3.174954 3.235097,-2.653498 1.474927,3.915545 3.947547,-1.387004 0.04678,4.183864 4.183863,0.04678 -1.387004,3.947547 3.915545,1.474927 -2.653498,3.235097 3.174955,2.725173 -3.599942,2.132447 2.051418,3.646724 -4.112178,0.772592 z" />
      <text
         xml:space="preserve"
         style="font-size:16px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;letter-spacing:-1.32000005px;writing-mode:lr-tb;text-anchor:start;opacity:0.15;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         x="59.530632"
         y="77.325226"
         id="text3856"
         sodipodi:linespacing="125%"
         transform="scale(0.9999961,1.0000039)">         <tspan
   sodipodi:role="line"
   id="tspan3858"
   x="59.530632"
   y="77.325226"
   style="font-size:16px;font-weight:bold;letter-spacing:-1.32000005px;fill:#000000;-inkscape-font-specification:Sans Bold">{0}</tspan>       </text>
      <path
         style="opacity:0;fill:#000000;stroke:none;display:inline"
         id="path3919"
         inkscape:connector-curvature="0"
         d="m 60,72 4,-4 4,4 8,-8 4,4 -12,12 -8,-8 z" />
      <path
         style="opacity:0.6;color:#000000;fill:url(#linearGradient3948);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3933"
         inkscape:connector-curvature="0"
         d="M 71.5625,52 68.71875,55.34375 65.3125,52.5625 63.78125,56.65625 59.625,55.1875 l 0,1 4.15625,1.46875 1.53125,-4.09375 3.40625,2.78125 L 71.5625,53 73.8125,56.78125 77.625,54.625 78.4375,58.9375 82.625,58.25 82.78125,57.21875 78.4375,57.9375 77.625,53.625 73.8125,55.78125 71.5625,52 z m -11.96875,7.59375 -4.40625,0.03125 0.34375,1 4.0625,-0.03125 0,-1 z m 22.625,2 -0.15625,0.96875 3.8125,0.71875 0.5,-0.90625 -4.15625,-0.78125 z m -25.875,2.3125 -3.78125,1.40625 0.625,0.78125 3.46875,-1.3125 -0.3125,-0.875 z m 28.3125,2.53125 -0.4375,0.75 3.09375,1.84375 L 88,68.4375 l -3.34375,-2 z M 54.875,69.125 52,71.5625 l 0.6875,0.40625 2.65625,-2.25 L 54.875,69.125 z m 30.25,2.75 -0.46875,0.40625 2.15625,2.625 0.625,-0.21875 -2.3125,-2.8125 z m -29.78125,2.6875 -1.71875,3.0625 0.5,0.09375 1.65625,-2.90625 -0.4375,-0.25 z m 28.3125,2.53125 -0.3125,0.125 1.125,3.15625 0.34375,0 -1.15625,-3.28125 z m -25.875,2.3125 -0.5625,3.375 L 57.375,82.75 57.9375,79.4375 57.78125,79.40625 z" />
      <text
         xml:space="preserve"
         style="font-size:12px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;opacity:0.3;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         x="60.261475"
         y="76.597481"
         id="text3074"
         sodipodi:linespacing="125%">         <tspan
   sodipodi:role="line"
   id="tspan3076"
   x="60.261475"
   y="76.597481"
   style="font-size:14px;fill:#000000">{0}</tspan>       </text>
      <text
         transform="scale(0.9999961,1.0000039)"
         sodipodi:linespacing="125%"
         id="text3852"
         y="78.053253"
         x="58.71452"
         style="font-size:18px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;letter-spacing:-1.32000005px;writing-mode:lr-tb;text-anchor:start;opacity:0.05;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         xml:space="preserve">         <tspan
   style="font-size:18px;font-weight:bold;letter-spacing:-2.47000003px;fill:#000000;-inkscape-font-specification:Sans Bold"
   y="78.053253"
   x="58.71452"
   id="tspan3854"
   sodipodi:role="line">{0}</tspan>       </text>
      <text
         sodipodi:linespacing="125%"
         id="text3070"
         y="76.097481"
         x="60.261475"
         style="font-size:12px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;fill:#ff0000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         xml:space="preserve">         <tspan
   style="font-size:14px;fill:#ffffff"
   y="76.097481"
   x="60.261475"
   id="tspan3072"
   sodipodi:role="line">{0}</tspan>       </text>
    </g>
  </g>
</svg>"""
    formated_counter = str('%02d' % self.counter)
    return emblem_string.format(formated_counter)     # replaces the '{0}' on the triple-quoted http://stackoverflow.com/questions/3877623/in-python-can-you-have-variables-within-triple-quotes-if-so-how
    
  def draw_large(self):
    emblem_string = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="120"
   height="120"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.2 r9819">
  <defs
     id="defs4">
    <linearGradient
       x1="68"
       y1="52"
       x2="68"
       y2="84"
       id="linearGradient3948"
       xlink:href="#linearGradient3942"
       gradientUnits="userSpaceOnUse" />
    <linearGradient
       id="linearGradient3942">
      <stop
         id="stop3944"
         style="stop-color:#ffffff;stop-opacity:1"
         offset="0" />
      <stop
         id="stop3946"
         style="stop-color:#ffffff;stop-opacity:0"
         offset="1" />
    </linearGradient>
  </defs>
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="2.8"
     inkscape:cx="113.74708"
     inkscape:cy="53.985929"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     fit-margin-top="0"
     fit-margin-left="0"
     fit-margin-right="0"
     fit-margin-bottom="0"
     inkscape:window-width="1280"
     inkscape:window-height="775"
     inkscape:window-x="0"
     inkscape:window-y="1"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Camada 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-294.28571,-203.79074)">
    <image
       y="203.79074"
       x="294.28571"
       id="image3066"
       xlink:href="./icon"
       height="120"
       width="120" />
    <g
       id="g3234"
       transform="matrix(2.5373346,0,0,2.7635428,176.61279,68.718501)">
      <path
         style="opacity:0.1;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3960"
         inkscape:connector-curvature="0"
         d="m 89.986349,69.238985 c -0.21488,-1.561093 -1.973583,-1.971086 -3.08095,-2.785965 0.452305,-1.002477 1.307299,-1.880744 1.442147,-2.982622 0.09844,-1.212445 -1.013508,-2.114893 -2.161243,-2.135756 -0.574938,-0.191984 -1.529962,-0.121132 -1.883184,-0.466436 0.105461,-1.303923 0.927598,-2.804937 -0.05258,-3.95302 -0.907896,-1.060888 -2.339545,-0.509432 -3.503632,-0.325674 -0.950635,0.504422 -0.81239,-0.565783 -0.973216,-1.2035 -0.130627,-1.071533 -0.401383,-2.422333 -1.652276,-2.666162 -1.269606,-0.351715 -2.257329,0.785416 -3.345553,1.248885 -0.564682,0.197811 -0.761585,-1.032508 -1.178359,-1.409042 -0.426005,-1.011804 -1.521655,-1.848863 -2.654045,-1.413094 -1.095119,0.436651 -1.63445,1.627605 -2.458205,2.425428 -0.973647,-0.65486 -1.72467,-1.7847 -2.91707,-1.99934 -1.243767,-0.181639 -2.134633,0.905175 -2.372989,2.019516 -0.345055,0.444832 -0.243497,1.842522 -1.003052,1.403006 -1.213096,-0.355405 -2.631658,-1.302577 -3.801916,-0.341572 -1.164288,0.944179 -0.641361,2.603822 -0.785903,3.912444 -1.186176,0.269467 -2.880347,-0.340038 -3.868298,0.741757 -1.026659,1.143887 -0.143349,2.597452 0.237559,3.813095 0.487992,0.76899 -0.891072,0.672735 -1.319748,1.016916 -1.098052,0.268634 -2.195073,1.121664 -2.064313,2.380723 0.249354,1.192288 1.335753,1.97237 1.99934,2.949845 -0.871859,0.915157 -2.269562,1.493314 -2.556533,2.818742 -0.186067,1.142981 0.709312,1.986005 1.663193,2.403037 0.374257,0.418594 1.762649,0.565214 1.196802,1.235928 -0.585967,1.153839 -1.765734,2.450576 -0.926208,3.768425 0.810341,1.207354 2.476744,0.956157 3.736472,1.311043 -0.08576,1.227497 -0.781478,2.521328 -0.229433,3.703695 0.526899,1.071756 1.844115,1.213477 2.87647,0.879241 0.560732,0.07218 1.729076,-0.722239 1.724808,0.155757 0.28962,1.207178 0.140911,2.908592 1.527846,3.422546 1.38487,0.596205 2.576146,-0.697698 3.773565,-1.225564 0.454783,0.276534 0.742145,1.177337 1.132089,1.695641 0.455828,1.285443 2.259105,1.820804 3.255585,0.80819 0.610876,-0.645848 1.17573,-1.360459 1.769908,-2.032116 1.070537,0.696774 1.92142,2.036743 3.310382,1.999339 1.284689,-0.0939 1.81764,-1.335721 2.151522,-2.404812 0.206115,-0.763429 0.45194,-1.441171 1.291319,-0.838121 1.079697,0.400421 2.40691,1.016712 3.407356,0.09643 1.036768,-1.007403 0.54752,-2.574581 0.688297,-3.867575 1.24572,-0.135375 2.670869,0.29881 3.736472,-0.524417 0.936001,-0.804307 0.694064,-2.129136 0.219537,-3.122161 -0.129526,-0.619425 -0.912001,-1.544893 0.15361,-1.604149 1.111548,-0.448238 2.718145,-0.69704 2.904459,-2.123887 0.293747,-1.438242 -1.158981,-2.317711 -1.863365,-3.381883 -0.0012,-0.497479 0.978512,-0.910082 1.354831,-1.374896 0.68176,-0.486375 1.154931,-1.160958 1.098503,-2.027866 z" />
      <path
         inkscape:connector-curvature="0"
         style="opacity:0.15;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3956"
         transform="matrix(0,1.048834,-1.048834,0,146.16452,5.4895435)"
         d="m 60.9375,54.59375 a 0.86264402,0.86264402 0 0 0 -0.71875,0.4375 L 58.5,57.875 55.625,56.25 a 0.86264402,0.86264402 0 0 0 -1.28125,0.59375 l -0.625,3.3125 -3.28125,-0.5625 a 0.86264402,0.86264402 0 0 0 -1,1 L 50,63.875 46.6875,64.5 a 0.86264402,0.86264402 0 0 0 -0.59375,1.28125 l 1.625,2.875 L 44.875,70.375 A 0.86264402,0.86264402 0 0 0 44.75,71.78125 L 47.25,73.9375 45.15625,76.5 A 0.86264402,0.86264402 0 0 0 45.5,77.875 l 3.15625,1.1875 -1.125,3.15625 a 0.86264402,0.86264402 0 0 0 0.8125,1.15625 l 3.3125,0.03125 0.0625,3.3125 a 0.86264402,0.86264402 0 0 0 1.15625,0.8125 L 56,86.4375 l 1.1875,3.125 a 0.86264402,0.86264402 0 0 0 1.34375,0.34375 l 2.59375,-2.125 2.1875,2.5625 a 0.86264402,0.86264402 0 0 0 1.40625,-0.125 l 1.6875,-2.875 2.9375,1.625 a 0.86264402,0.86264402 0 0 0 1.25,-0.59375 l 0.59375,-3.28125 3.3125,0.5625 a 0.86264402,0.86264402 0 0 0 1,-1 L 74.9375,81.34375 78.21875,80.75 A 0.86264402,0.86264402 0 0 0 78.8125,79.5 l -1.625,-2.9375 2.875,-1.6875 a 0.86264402,0.86264402 0 0 0 0.125,-1.40625 L 77.625,71.28125 79.75,68.6875 a 0.86264402,0.86264402 0 0 0 -0.34375,-1.34375 l -3.125,-1.1875 1.09375,-3.125 A 0.86264402,0.86264402 0 0 0 76.5625,61.875 L 73.25,61.8125 73.21875,58.5 A 0.86264402,0.86264402 0 0 0 72.0625,57.6875 l -3.15625,1.125 -1.1875,-3.15625 a 0.86264402,0.86264402 0 0 0 -1.375,-0.34375 l -2.5625,2.09375 -2.15625,-2.5 a 0.86264402,0.86264402 0 0 0 -0.6875,-0.3125 z" />
      <path
         inkscape:connector-curvature="0"
         style="opacity:0.3;color:#000000;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3950"
         transform="matrix(0,1.048834,-1.048834,0,146.16452,5.4895435)"
         d="m 74.641931,84.79994 -4.128425,-0.680449 -0.772592,4.112178 -3.646724,-2.051417 -2.132447,3.599941 -2.725174,-3.174954 -3.235096,2.653498 -1.474928,-3.915545 -3.947546,1.387004 -0.04678,-4.183864 -4.183864,-0.04678 1.387005,-3.947547 -3.915546,-1.474927 2.653499,-3.235097 -3.174955,-2.725173 3.599941,-2.132447 -2.051417,-3.646724 4.112178,-0.772592 -0.680448,-4.128426 4.128425,0.680449 0.772592,-4.112178 3.646724,2.051417 2.132447,-3.599941 2.725173,3.174954 3.235097,-2.653498 1.474927,3.915545 3.947547,-1.387004 0.04678,4.183864 4.183863,0.04678 -1.387004,3.947547 3.915545,1.474927 -2.653498,3.235097 3.174955,2.725173 -3.599942,2.132447 2.051418,3.646724 -4.112178,0.772592 z" />
      <path
         transform="matrix(0,1.048834,-1.048834,0,146.16452,4.4895435)"
         inkscape:connector-curvature="0"
         style="color:#000000;fill:#ff0000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3139"
         d="m 74.641931,84.79994 -4.128425,-0.680449 -0.772592,4.112178 -3.646724,-2.051417 -2.132447,3.599941 -2.725174,-3.174954 -3.235096,2.653498 -1.474928,-3.915545 -3.947546,1.387004 -0.04678,-4.183864 -4.183864,-0.04678 1.387005,-3.947547 -3.915546,-1.474927 2.653499,-3.235097 -3.174955,-2.725173 3.599941,-2.132447 -2.051417,-3.646724 4.112178,-0.772592 -0.680448,-4.128426 4.128425,0.680449 0.772592,-4.112178 3.646724,2.051417 2.132447,-3.599941 2.725173,3.174954 3.235097,-2.653498 1.474927,3.915545 3.947547,-1.387004 0.04678,4.183864 4.183863,0.04678 -1.387004,3.947547 3.915545,1.474927 -2.653498,3.235097 3.174955,2.725173 -3.599942,2.132447 2.051418,3.646724 -4.112178,0.772592 z" />
      <text
         xml:space="preserve"
         style="font-size:16px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;letter-spacing:-1.32000005px;writing-mode:lr-tb;text-anchor:start;opacity:0.15;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         x="59.530632"
         y="77.325226"
         id="text3856"
         sodipodi:linespacing="125%"
         transform="scale(0.9999961,1.0000039)">         <tspan
   sodipodi:role="line"
   id="tspan3858"
   x="59.530632"
   y="77.325226"
   style="font-size:16px;font-weight:bold;letter-spacing:-1.32000005px;fill:#000000;-inkscape-font-specification:Sans Bold">{0}</tspan>       </text>
      <path
         style="opacity:0;fill:#000000;stroke:none;display:inline"
         id="path3919"
         inkscape:connector-curvature="0"
         d="m 60,72 4,-4 4,4 8,-8 4,4 -12,12 -8,-8 z" />
      <path
         style="opacity:0.6;color:#000000;fill:url(#linearGradient3948);fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
         id="path3933"
         inkscape:connector-curvature="0"
         d="M 71.5625,52 68.71875,55.34375 65.3125,52.5625 63.78125,56.65625 59.625,55.1875 l 0,1 4.15625,1.46875 1.53125,-4.09375 3.40625,2.78125 L 71.5625,53 73.8125,56.78125 77.625,54.625 78.4375,58.9375 82.625,58.25 82.78125,57.21875 78.4375,57.9375 77.625,53.625 73.8125,55.78125 71.5625,52 z m -11.96875,7.59375 -4.40625,0.03125 0.34375,1 4.0625,-0.03125 0,-1 z m 22.625,2 -0.15625,0.96875 3.8125,0.71875 0.5,-0.90625 -4.15625,-0.78125 z m -25.875,2.3125 -3.78125,1.40625 0.625,0.78125 3.46875,-1.3125 -0.3125,-0.875 z m 28.3125,2.53125 -0.4375,0.75 3.09375,1.84375 L 88,68.4375 l -3.34375,-2 z M 54.875,69.125 52,71.5625 l 0.6875,0.40625 2.65625,-2.25 L 54.875,69.125 z m 30.25,2.75 -0.46875,0.40625 2.15625,2.625 0.625,-0.21875 -2.3125,-2.8125 z m -29.78125,2.6875 -1.71875,3.0625 0.5,0.09375 1.65625,-2.90625 -0.4375,-0.25 z m 28.3125,2.53125 -0.3125,0.125 1.125,3.15625 0.34375,0 -1.15625,-3.28125 z m -25.875,2.3125 -0.5625,3.375 L 57.375,82.75 57.9375,79.4375 57.78125,79.40625 z" />
      <text
         xml:space="preserve"
         style="font-size:12px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;opacity:0.3;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         x="60.261475"
         y="76.597481"
         id="text3074"
         sodipodi:linespacing="125%">         <tspan
   sodipodi:role="line"
   id="tspan3076"
   x="60.261475"
   y="76.597481"
   style="font-size:14px;fill:#000000">{0}</tspan>       </text>
      <text
         transform="scale(0.9999961,1.0000039)"
         sodipodi:linespacing="125%"
         id="text3852"
         y="78.053253"
         x="58.71452"
         style="font-size:18px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;letter-spacing:-1.32000005px;writing-mode:lr-tb;text-anchor:start;opacity:0.05;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         xml:space="preserve">         <tspan
   style="font-size:18px;font-weight:bold;letter-spacing:-2.47000003px;fill:#000000;-inkscape-font-specification:Sans Bold"
   y="78.053253"
   x="58.71452"
   id="tspan3854"
   sodipodi:role="line">{0}</tspan>       </text>
      <text
         sodipodi:linespacing="125%"
         id="text3070"
         y="76.097481"
         x="60.261475"
         style="font-size:12px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;fill:#ff0000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Sans;-inkscape-font-specification:Sans Bold"
         xml:space="preserve">         <tspan
   style="font-size:14px;fill:#ffffff"
   y="76.097481"
   x="60.261475"
   id="tspan3072"
   sodipodi:role="line">{0}</tspan>       </text>
    </g>
  </g>
</svg>"""
    formated_counter = str('%02d' % self.counter)
    return emblem_string.format(formated_counter)     # replaces the '{0}' on the triple-quoted http://stackoverflow.com/questions/3877623/in-python-can-you-have-variables-within-triple-quotes-if-so-how
