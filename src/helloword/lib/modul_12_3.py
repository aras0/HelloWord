# -*- coding: utf-8 -*-

import sys
from xml.dom.minidom import parseString
import urllib , urllib2
import xml_tree as xtre
import getopt

# python modul-12_3.py canon1100d a8839b1180ea00fa1cf7c6b74ca01bb5
# python modul_12_3.py canon1100d a8839b1180ea00fa1cf7c6b74ca01bb5

# python modul_12_3.py -o canon1100d -n a8839b1180ea00fa1cf7c6b74ca01bb5
# python modul_12_3.py macbook a8839b1180ea00fa1cf7c6b74ca01bb5

def sortedDictValues3(adict):
    keys = adict.keys()
    keys.sort()
    print keys
    return keys[0]


def drukujSlownik(adict):
    for klucz, wartosc in slownik.items():
        print klucz, wartosc


def downlNokaut(przedmiot, key_number):
    """Return oferts
    >>>downlNokaut(canon1100d, a8839b1180ea00fa1cf7c6b74ca01bb5)
    35.0 http://www.nokaut.pl/ochrona-wyswietlacza-aparatu/oslona-na-wyswietlacz-canon-1100d.html
    """
    a_url = 'http://api.nokaut.pl/?format=xml&key=' + key_number + \
    '&method=nokaut.product.getByKeyword&keyword='+przedmiot+'&filters[price_min]'
#http://api.nokaut.pl/?format=xml&key=a8839b1180ea00fa1cf7c6b74ca01bb5&method=nokaut.product.getByKeyword&keyword=canon1100d&filters[price_min]
    #root = etree.Element("root")
    #print root




    file = urllib.urlopen(a_url)
    data = file.read()
    file.close()
    dom = parseString(data)
    slownik=dict()
    price_min=float()
    cNodes = dom.childNodes
    price_min = dom.getElementsByTagName("price_min")[0].childNodes[0].toxml()

    for i in cNodes[0].getElementsByTagName("item"):
        li=list()
        li.extend([i.getElementsByTagName("name")[0].childNodes[0].toxml(), i.getElementsByTagName("url")[0].childNodes[0].toxml(), i.getElementsByTagName("image_mini")[0].childNodes[0].toxml()])
        price_min = i.getElementsByTagName("price_min")[0].childNodes[0].toxml()
        price = price_min.replace(',','.')
        price_min = float(price)
        slownik.update({price_min:li})
    k=sortedDictValues3(slownik)


    #drukujSlownik(slownik)


    for klucz, wartosc in slownik.items():
        if klucz==k:
            print klucz, wartosc[1:]
            return klucz, wartosc[1:]

def usage():
        usage = """
        -h --help                 Prints this help
        -o --objects              Print objects
        -n --argument -API key    Print argument
        """
        print usage

def end():
    sys.exit(2)

def main():
    """main
    >>>main()

    """
    if len(sys.argv)==3 or len(sys.argv)==5:
        
    #if len(sys.argv)==4 or len(sys.argv)==6:
        #print sys.argv[3].join(sys.argv[4])
        i = 0
        try:
            opts, argsy = getopt.getopt(sys.argv[1:], 'ho:n:', ["help"])
            #print len(opts)
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        for opt, args in opts:
            if opt in ("--help", "-h"):
                return usage()
            if opt in ("-o"):

                nazwa = args
                #print nazwa
                i = i + 1
            if opt in ("-n"):
                num = args
                #print num
                i = i + 1

        if i == 2:
            print nazwa
            print num
            return downlNokaut(nazwa, num)

        if i == 0:
            nazwa = sys.argv[1]
            num = sys.argv[2]
            print nazwa
            print num

            return downlNokaut(nazwa, num)
    else:
        print len(sys.argv)



if __name__ == '__main__':
    main()
    
        #raise SystemExit, "Wrong number of arguments"
    #nazwa = str(sys.argv[1])
    #num = str(sys.argv[2])
    #print downl(nazwa , num)