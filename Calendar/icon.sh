#!/bin/bash

# This is a part of the external applet Calendar for Cairo-Dock
#
# Copyright : (C) 2009-2012 by Royohboy & Matttbe
#                         inspired of the icon of arkham
# E-mail : werbungfuerroy@googlemail.com and matttbe@gmail.com
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# http://www.gnu.org/licenses/licenses.html#GPL

ICON_DIR=$1
FORCE=$2
date_TODAY=`date '+%Y%m%d'`
# get current day and month
MONTH=$(date +%b)
DAY=$(date +%d)

# generate calendar-icon showing current day and month
make_icon() {
printf "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->
<svg
   xmlns:svg=\"http://www.w3.org/2000/svg\"
   xmlns=\"http://www.w3.org/2000/svg\"
   xmlns:xlink=\"http://www.w3.org/1999/xlink\"
   version=\"1.0\"
   width=\"128\"
   height=\"128\"
   id=\"svg2\">
  <defs
     id=\"defs4\">
    <linearGradient
       id=\"linearGradient3999\">
      <stop
         id=\"stop4001\"
         style=\"stop-color:#626262;stop-opacity:1\"
         offset=\"0\" />
      <stop
         id=\"stop4003\"
         style=\"stop-color:#6c6865;stop-opacity:1\"
         offset=\"0.71532845\" />
      <stop
         id=\"stop4005\"
         style=\"stop-color:#5a5858;stop-opacity:1\"
         offset=\"0.81714529\" />
      <stop
         id=\"stop4007\"
         style=\"stop-color:#262626;stop-opacity:1\"
         offset=\"1\" />
    </linearGradient>
    <linearGradient
       id=\"linearGradient3973\">
      <stop
         id=\"stop3975\"
         style=\"stop-color:#b30000;stop-opacity:1\"
         offset=\"0\" />
      <stop
         id=\"stop3977\"
         style=\"stop-color:#ee3c3c;stop-opacity:1\"
         offset=\"0.71532845\" />
      <stop
         id=\"stop3979\"
         style=\"stop-color:#e66767;stop-opacity:1\"
         offset=\"0.81714529\" />
      <stop
         id=\"stop3981\"
         style=\"stop-color:#ff7171;stop-opacity:1\"
         offset=\"1\" />
    </linearGradient>
    <linearGradient
       id=\"linearGradient3955\">
      <stop
         id=\"stop3957\"
         style=\"stop-color:#1f1f1f;stop-opacity:1\"
         offset=\"0\" />
      <stop
         id=\"stop3959\"
         style=\"stop-color:#8f8b88;stop-opacity:1\"
         offset=\"0.71532845\" />
      <stop
         id=\"stop3961\"
         style=\"stop-color:#a7a5a5;stop-opacity:1\"
         offset=\"0.81714529\" />
      <stop
         id=\"stop3963\"
         style=\"stop-color:#c9c9c9;stop-opacity:1\"
         offset=\"1\" />
    </linearGradient>
    <linearGradient
       id=\"linearGradient3410\">
      <stop
         id=\"stop3412\"
         style=\"stop-color:#ffffff;stop-opacity:1\"
         offset=\"0\" />
      <stop
         id=\"stop3420\"
         style=\"stop-color:#d1cfce;stop-opacity:1\"
         offset=\"0.71532845\" />
      <stop
         id=\"stop3422\"
         style=\"stop-color:#a7a5a5;stop-opacity:1\"
         offset=\"0.89402735\" />
      <stop
         id=\"stop3414\"
         style=\"stop-color:#696969;stop-opacity:1\"
         offset=\"1\" />
    </linearGradient>
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient3416\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient3935\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient3943\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\" />
    <linearGradient
       x1=\"164.1438\"
       y1=\"837.71381\"
       x2=\"262.08289\"
       y2=\"837.71381\"
       id=\"linearGradient3951\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\" />
    <linearGradient
       x1=\"288.1875\"
       y1=\"767.53125\"
       x2=\"382.15625\"
       y2=\"767.53125\"
       id=\"linearGradient3971\"
       xlink:href=\"#linearGradient3973\"
       gradientUnits=\"userSpaceOnUse\" />
    <linearGradient
       x1=\"298.21402\"
       y1=\"843.86743\"
       x2=\"401.52759\"
       y2=\"843.86743\"
       id=\"linearGradient3997\"
       xlink:href=\"#linearGradient3999\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"translate(0,-0.3181177)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient4027\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(0.9853821,-0.170359,0.170359,0.9853821,9.129394e-2,1.6818823)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient4031\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(0.9853821,-0.170359,0.170359,0.9853821,-0.4536475,3.3637646)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4035\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4050\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4052\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4054\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4056\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient4079\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(0.9853821,-0.170359,0.170359,0.9853821,-0.4536475,3.3637646)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient4081\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(0.9853821,-0.170359,0.170359,0.9853821,9.129394e-2,1.6818823)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient4083\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\" />
    <linearGradient
       x1=\"164.1438\"
       y1=\"837.71381\"
       x2=\"262.08289\"
       y2=\"837.71381\"
       id=\"linearGradient4085\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\" />
    <linearGradient
       x1=\"288.1875\"
       y1=\"767.53125\"
       x2=\"382.15625\"
       y2=\"767.53125\"
       id=\"linearGradient4087\"
       xlink:href=\"#linearGradient3973\"
       gradientUnits=\"userSpaceOnUse\" />
    <linearGradient
       x1=\"298.21402\"
       y1=\"843.86743\"
       x2=\"401.52759\"
       y2=\"843.86743\"
       id=\"linearGradient4089\"
       xlink:href=\"#linearGradient3999\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"translate(0,-0.3181177)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4091\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4093\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4095\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient4097\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient2476\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient2478\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient2480\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <radialGradient
       cx=\"302.849\"
       cy=\"753.43823\"
       r=\"4.0006304\"
       fx=\"302.849\"
       fy=\"753.43823\"
       id=\"radialGradient2482\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(1,0,0,2.9350391,0,-1457.9325)\" />
    <linearGradient
       x1=\"298.21402\"
       y1=\"843.86743\"
       x2=\"401.52759\"
       y2=\"843.86743\"
       id=\"linearGradient2493\"
       xlink:href=\"#linearGradient3999\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"translate(-279.19683,-729.67545)\" />
    <linearGradient
       x1=\"288.1875\"
       y1=\"767.53125\"
       x2=\"382.15625\"
       y2=\"767.53125\"
       id=\"linearGradient2500\"
       xlink:href=\"#linearGradient3973\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"translate(-279.19683,-729.35733)\" />
    <linearGradient
       x1=\"164.1438\"
       y1=\"837.71381\"
       x2=\"262.08289\"
       y2=\"837.71381\"
       id=\"linearGradient2503\"
       xlink:href=\"#linearGradient3410\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(0.9873932,-0.1582869,0.1582869,0.9873932,-279.19683,-729.35733)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient2506\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(0.9853821,-0.170359,0.170359,0.9853821,-279.19683,-729.35733)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient2509\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(0.9853821,-0.170359,0.170359,0.9853821,-279.10554,-727.67545)\" />
    <linearGradient
       x1=\"154.15988\"
       y1=\"851.48376\"
       x2=\"249.32434\"
       y2=\"851.48376\"
       id=\"linearGradient2512\"
       xlink:href=\"#linearGradient3955\"
       gradientUnits=\"userSpaceOnUse\"
       gradientTransform=\"matrix(0.9853821,-0.170359,0.170359,0.9853821,-279.65048,-725.99357)\" />
  </defs>
  <path
     d=\"M 5.6692384,34.821242 L 100.61614,19.015668 L 122.29976,103.02618 L 18.769049,122.26528 L 5.6692384,34.821242 z\"
     id=\"rect3379\"
     style=\"fill:#1a1a1a;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1\" />
  <path
     d=\"M 13.60118,58.37304 L 99.70868,43.28563 L 115.50468,99.05508 L 22.71671,115.09685 L 13.60118,58.37304 z\"
     id=\"path4029\"
     style=\"fill:url(#linearGradient2512);fill-opacity:1;stroke:#000000;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1\" />
  <path
     d=\"M 14.14612,56.69116 L 100.25362,41.60375 L 116.04962,97.3732 L 23.26165,113.41497 L 14.14612,56.69116 z\"
     id=\"path4025\"
     style=\"fill:url(#linearGradient2509);fill-opacity:1;stroke:#1a1a1a;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1\" />
  <path
     d=\"M 14.054826,55.009283 L 100.16233,39.921869 L 115.95833,95.691324 L 23.170357,111.73309 L 14.054826,55.009283 z\"
     id=\"rect3391\"
     style=\"fill:url(#linearGradient2506);fill-opacity:1;stroke:#333333;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1\" />
  <path
     d=\"M 9.4772803,31.230194 L 95.89434,17.010764 C 101.84451,42.988204 110.19816,74.459282 116.49168,86.359252 C 92.930711,94.418142 53.292256,104.88049 22.520865,112.59603 L 9.4772803,31.230194 z\"
     id=\"rect2606\"
     style=\"fill:url(#linearGradient2503);fill-opacity:1;stroke:#000000;stroke-width:0.99999994;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />
  <path
     d=\"M 95.469118,17.160271 L 9.6332705,31.521621 L 14.394005,59.229336 L 102.03162,43.513718 C 99.686648,34.585548 97.446918,25.794991 95.469118,17.160271 z\"
     id=\"path3382\"
     style=\"fill:url(#linearGradient2500);fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />
  <text
     x=\"12.788574\"
     y=\"57.323757\"
     transform=\"matrix(0.9877179,-0.156248,0.156248,0.9877179,0,0)\"
     id=\"text2602\"
     xml:space=\"preserve\"
     style=\"font-size:16px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:condensed;text-align:start;line-height:125%%;writing-mode:lr-tb;text-anchor:start;fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;font-family:Nimbus Sans L;-inkscape-font-specification:Nimbus Sans L Bold Condensed\"><tspan
       x=\"12.788574\"
       y=\"57.323757\"
       id=\"tspan2604\">$MONTH</tspan></text>
  <text
     x=\"48.404499\"
     y=\"101.66183\"
     transform=\"matrix(0.9853867,-0.1703323,0.1703323,0.9853867,0,0)\"
     id=\"text2598\"
     xml:space=\"preserve\"
     style=\"font-size:48px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;line-height:125%%;writing-mode:lr-tb;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;font-family:Nimbus Sans L;-inkscape-font-specification:Nimbus Sans L Bold\"><tspan
       x=\"48.404499\"
       y=\"101.66183\"
       id=\"tspan2600\"
       style=\"font-size:48px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;line-height:125%%;writing-mode:lr-tb;text-anchor:middle;font-family:Nimbus Sans L;-inkscape-font-specification:Nimbus Sans L Bold\">$DAY</tspan></text>
  <path
     d=\"M 18.86917,122.25144 L 122.33076,102.71524 L 122.1116,106.50708 L 19.39588,125.71812 L 18.86917,122.25144 z\"
     id=\"rect3388\"
     style=\"fill:url(#linearGradient2493);fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1\" />
  <g
     transform=\"translate(-279.19683,-729.35733)\"
     id=\"g4037\">
    <path
       d=\"M 311.75531,764.14758 C 311.75703,765.39866 310.90855,766.55528 309.52988,767.18121 C 308.15121,767.80714 306.45212,767.80714 305.07345,767.18121 C 303.69478,766.55528 302.8463,765.39866 302.84802,764.14758 C 302.8463,762.8965 303.69478,761.73988 305.07345,761.11395 C 306.45212,760.48802 308.15121,760.48802 309.52988,761.11395 C 310.90855,761.73988 311.75703,762.8965 311.75531,764.14758 L 311.75531,764.14758 z\"
       transform=\"matrix(0.9005081,0,0,0.9642831,31.051186,27.452039)\"
       id=\"path3394\"
       style=\"fill:#000000;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />
    <path
       d=\"M 299.36,755.25543 C 299.22202,749.33101 300.35118,743.93902 302.02321,742.53808 C 303.69524,741.13714 305.41401,744.14293 306.07704,749.62743 C 306.74007,755.11193 306.15063,761.44779 304.6868,764.57096\"
       transform=\"matrix(0.7921082,-0.1723206,0.1261344,1.0821514,-28.999117,-9.1242685)\"
       id=\"path3398\"
       style=\"fill:none;fill-opacity:1;stroke:url(#radialGradient2476);stroke-width:3.86078405;stroke-linecap:round;marker-start:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />
    <path
       d=\"M 299.36,755.25543 C 299.22202,749.33101 300.35118,743.93902 302.02321,742.53808 C 303.69524,741.13714 305.41401,744.14293 306.07704,749.62743 C 306.74007,755.11193 306.15063,761.44779 304.6868,764.57096\"
       transform=\"matrix(0.7921082,-0.1723206,0.1261344,1.0821514,-30.209688,-9.1242685)\"
       id=\"path4033\"
       style=\"fill:none;fill-opacity:1;stroke:url(#radialGradient2478);stroke-width:3.86078405;stroke-linecap:round;marker-start:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />
  </g>
  <g
     transform=\"translate(-228.77569,-737.75204)\"
     id=\"g4042\">
    <path
       d=\"M 311.75531,764.14758 C 311.75703,765.39866 310.90855,766.55528 309.52988,767.18121 C 308.15121,767.80714 306.45212,767.80714 305.07345,767.18121 C 303.69478,766.55528 302.8463,765.39866 302.84802,764.14758 C 302.8463,762.8965 303.69478,761.73988 305.07345,761.11395 C 306.45212,760.48802 308.15121,760.48802 309.52988,761.11395 C 310.90855,761.73988 311.75703,762.8965 311.75531,764.14758 L 311.75531,764.14758 z\"
       transform=\"matrix(0.9005081,0,0,0.9642831,31.051186,27.452039)\"
       id=\"path4044\"
       style=\"fill:#000000;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />
    <path
       d=\"M 299.36,755.25543 C 299.22202,749.33101 300.35118,743.93902 302.02321,742.53808 C 303.69524,741.13714 305.41401,744.14293 306.07704,749.62743 C 306.74007,755.11193 306.15063,761.44779 304.6868,764.57096\"
       transform=\"matrix(0.7921082,-0.1723206,0.1261344,1.0821514,-28.999117,-9.1242685)\"
       id=\"path4046\"
       style=\"fill:none;fill-opacity:1;stroke:url(#radialGradient2480);stroke-width:3.86078405;stroke-linecap:round;marker-start:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />
    <path
       d=\"M 299.36,755.25543 C 299.22202,749.33101 300.35118,743.93902 302.02321,742.53808 C 303.69524,741.13714 305.41401,744.14293 306.07704,749.62743 C 306.74007,755.11193 306.15063,761.44779 304.6868,764.57096\"
       transform=\"matrix(0.7921082,-0.1723206,0.1261344,1.0821514,-30.209688,-9.1242685)\"
       id=\"path4048\"
       style=\"fill:none;fill-opacity:1;stroke:url(#radialGradient2482);stroke-width:3.86078405;stroke-linecap:round;marker-start:none;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />
  </g>
</svg>" > "$ICON_DIR/icon"

	dbus-send --session --dest=org.cairodock.CairoDock /org/cairodock/CairoDock org.cairodock.CairoDock.SetIcon string:"$ICON_DIR/icon" string:"module=Calendar"
	echo "$date_TODAY" > "$ICON_DIR/.day"
}

if test ! -e "$ICON_DIR/.day"; then
	# this file doesn't exist
	make_icon
elif [ `cat "$ICON_DIR/.day"` -lt $date_TODAY ];then
	# this file exists and the date is older
	make_icon
elif [ "$FORCE" = "1" ]; then
	make_icon
fi

exit
