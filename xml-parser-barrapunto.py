#!/usr/bin/python3
"""
Parseador XML para titulares de barrapunto.com
Javier Fernandez Morata
"""
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

class BarraPunto(ContentHandler):

    bodyHTML = "<!DOCTYPE HTMl><html><body>"

    def __init__(self):
        self.inContent = 0
        self.titulares = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.titulares = True
        elif self.titulares:
            if name == 'title':
                self.inContent = 1
            elif name == 'link':
                self.inContent = 1

    def endElement(self, name):
        if name == 'item':
            self.titulares = False
        elif self.titulares:
            if name == 'title':
                titulo = "<br> Titular: " + self.theContent + ".<br>"
                self.bodyHTML = self.bodyHTML + titulo
                self.inContent = 0
                self.theContent = ""
            elif name == 'link':
                enlace = "<a href=" + self.theContent + \
                        "> Enlace:" + self.theContent + "</a>.<br>"
                self.bodyHTML = self.bodyHTML + enlace
                self.inContent = 0
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

#MAIN PROG
if len(sys.argv) < 2:
    print ("Usage: ./xml-parser-barrapunto.py [document]")
    print
    print ("[document]: file name of the document to parse")
    sys.exit(1)

#Creamos el Objeto que parseara y el controlador

BarraPuntoParse = make_parser()
BarraPuntoHandler = BarraPunto()
BarraPuntoParse.setContentHandler(BarraPuntoHandler)

#Vamos alla

xmlFile = open(sys.argv[1], "r")
BarraPuntoParse.parse(xmlFile)
BarraPuntoHandler.bodyHTML = BarraPuntoHandler.bodyHTML + "</body></html>"
print(BarraPuntoHandler.bodyHTML)
