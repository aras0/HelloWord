#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import urllib
import urllib2
import xml_tree as xtre
from BeautifulSoup import BeautifulSoup
import re
#import mechanize

#python modul_13_1.py canon1100d
#python modul_13_1.py macbook
def loadAlegro(obiekt):
    li = list()
    a_url = 'http://allegro.pl/listing/listing.php?offerTypeBuyNow=1&order=p&standard_allegro=1&string='+obiekt
    response = urllib2.urlopen(a_url)
    html = response.read()
    soup = BeautifulSoup(html)


    #try:
        #soup.findAll("section", {"class" : "offers"})[1].find("div", {"class" : "excerpt"})
        #html4 = soup.findAll("section", {"class" : "offers"})[1].find("div", {"class" : "excerpt"})
    #except IndexError: 
        #soup.findAll("section", {"class" : "offers"})[0].find("div", {"class" : "excerpt"})
    sectionOffers = soup.findAll("section", {"class" : "offers"})
    print len(sectionOffers)
    if len(sectionOffers) == 2:

        #print sectionOffers[1]
        if sectionOffers[1].find("h2", {"class": "listing-header"}).string == "lista ofert":
            #print "true"

            html5 = sectionOffers[1].find("div", {"class" : "excerpt"})
            #print html5
            #finally:
            #f = open("aa.html", 'w')
            #f.write(html)

            cena = sectionOffers[1].find("span", {"class" : "buy-now dist"}).span.nextSibling
            print cena
            #html2 = soup.find("div", {"class" : "excerpt"})
            cena = cena.replace(',','.')

            print cena
            link = sectionOffers[1].find("div", {"class" : "details"}).header.h2.a['href']
            linkalegro = "http://www.allegro.pl"+link
            print linkalegro
            #f = open("aaa.html", 'w')

            img = sectionOffers[1].find("div", {"class" : "photo loading"})['data-img']
            img = img.split(',')
            img = img[1].replace('"','')
            print img
            li.extend([cena, linkalegro, img])
            return li
    if len(sectionOffers)==1:
        #if sectionOffers[0].find("h2", {"class": "listing-header"}).string == "lista ofert":
        print sectionOffers[0].find("h2", {"class": "listing-header"}).string
        cena = sectionOffers[0].find("span", {"class" : "buy-now dist"}).span.nextSibling
        cena = cena.replace(',','.')
        print cena
        link = sectionOffers[0].find("div", {"class" : "details"}).header.h2.a['href']
        linkalegro = "http://www.allegro.pl"+link
        print linkalegro
        img = sectionOffers[0].find("div", {"class" : "photo loading"})['data-img']
        img = img.split(',')
        img = img[1].replace('"','')
        print img
        li.extend([cena, linkalegro, img])
        return li
    if len(sectionOffers)==0:
        #if soup.find("p", {"class" :"main-message"}).string == 'Nasze oferty nie sprostały Twoim wymaganiom.':
            szukane = soup.find("p", {"class" :"main-message"}).string
            szukane = str(szukane)
            if re.search('Nasze oferty nie sprostały Twoim wymaganiom.', szukane):
                print szukane
                end()
                return szukane
        #f=open("aa.html", 'w')
        #f.write(soup)




def usage():
        usage = """
        -h --help                 Prints this help
        -o --objects              Print objects
        """
        print usage

def end():
    print"exit"
    sys.exit(2)

def main():
    """main
    >>>main()

    """
    i = 0
    try:
        opts, argsy = getopt.getopt(sys.argv[1:], 'ho:a:', ["help"])

    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, args in opts:

        if opt in ("--help", "-h"):
            return usage()

        if opt in ("-o"):
            nazwa = args
            i = i + 1
        else:
            print args
            nazwa = args
            print nazwa

    if i == 1:
        print nazwa
        return loadAlegro(nazwa)

    if i == 0:
        nazwa = sys.argv[1]
        print nazwa
        return loadAlegro(nazwa)


if __name__ == '__main__':

    main()