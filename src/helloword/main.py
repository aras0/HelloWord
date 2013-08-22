#!/usr/bin/python
# -*- coding: <encoding name> -*-

import webapp2
import cgi
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db
import lib.modul_13_1 as allegro
import lib.modul_12_3 as nokaut
import ast
import urllib
from datetime import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import sys
import logging
import wsgiref.handlers


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])
    #loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))


def doRender(handler, tname, values={}):
    temp = os.path.join(
        os.path.dirname(__file__),
        'mytemplates/' + tname)
    if not os.path.isfile(temp):
        return False
    # Make a copy and add the path
    newval = dict(values)
    newval['path'] = handler.request.path
    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True


def Login(self, user):
    if user:
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
    return url, url_linktext


def DropDB():
    query = Object.all()
    db.delete(query)


#-------------------------------------- models
# A Model for a Object
class Object(db.Model):
    """Models an individual Guestbook entry with author, content, and date. # or -> db.ReferenceProperty()"""
    author = db.EmailProperty()
    content = db.StringProperty()
    dates = db. DateTimeProperty(auto_now_add=True)
    licznik = db.IntegerProperty()
    lalegro = db.StringProperty()
    lnokaut = db.StringProperty()
    calegro = db.FloatProperty()
    cnokaut = db.FloatProperty()
    imgalegro = db.StringProperty()
    imgnokaut = db.StringProperty()


# A Model for a User - nie uzywanie na razie
class User(db.Model):
    account = db.StringProperty()
    password = db.StringProperty()
    name = db.StringProperty()
#-------------------------------------- class


class Render(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        webapp2.RequestHandler.__init__(self, *args, **kwargs)

    def render_template(self, template_file, template_values=None):
        template = JINJA_ENVIRONMENT.get_template(template_file)
        self.response.write(template.render(template_values))


class CreateUser(Render):
    def post(self):
        user = users.get_current_user()
        acct = self.request.get('account')
        pw = self.request.get('password')
        url, url_linktext = Login(self, user)

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
        }
        self.render_template('mytemplates/index_results.html', template_values=template_values)


class SearchPage(Render):
#-----------------------
# wyswietlenie formularza z mozliwoscia wszukania produktu
    def get(self):
        doRender(self, 'searchPage.html')

# wyszukanie(skrypt) i dodanie do bazy wzyszukanych obiektow
    def post(self):

        zmienna = self.request.get('content')
        user = users.get_current_user()
# skrypt allegro
        allegro1 = allegro.loadAlegro(zmienna)
        allegro2 = str(allegro1)
        allegro3 = [item.encode('ascii') for item in ast.literal_eval(allegro2)]
# skrypt nokaut
        nok = nokaut.downlNokaut(self.request.get('content'), 'a8839b1180ea00fa1cf7c6b74ca01bb5')

# tworzenie zmiennych -dodanie do bazy
        cenaAll = allegro3[0]
        linkAll = allegro3[1]
        imgAll = allegro3[2]

        cenaNok = nok[0]
        Nok = nok[1]
        linkNok = Nok[0]
        imgNok = Nok[1]

        cenaAll = float(cenaAll)
        cenaNok = float(cenaNok)

# dodanie do bazy wyniku wyszukania
        obj = Object()
        if user:
            aut = user.email()
            obj.author = aut
            #self.response.write('<p> author %s </p>' % aut)

        obj.content = zmienna
        # a = Object.all()
        #produkty = a.filter('content =', zmienna).count()
        policz = 1
        query2 = db.Query(Object).order('-dates')
        for q2 in query2:
            # self.response.write('<a> licznik %s</a>' % (q2.author))

            if q2.content == zmienna:
                policz = policz + 1

        self.response.write('<a>licznik %s %s </a>' % (zmienna, policz))

        obj.lalegro = linkAll
        obj.lnokaut = linkNok
        obj.calegro = cenaAll
        obj.cnokaut = cenaNok
        obj.imgalegro = imgAll
        obj.imgnokaut = imgNok
        obj.licznik = policz
        obj.put()

        doRender(self, 'searchPage.html')

''' Model Object
            author = db.StringProperty()
            content = db.StringProperty(multiline=True)
            dates = db.DateProperty(auto_now_add=True)
            licznik = db.IntegerProperty()
            lalegro = db.StringProperty()
            lnokaut = db.StringProperty()
            calegro = db.StringProperty()
            cnokaut = db.StringProperty()'''


class ResultsPage(Render):
    # def post(self):
    #     g = Object()
    #     zmienna = self.request.get('content')
    #     user = users.get_current_user()
    #     url, url_linktext = Login(self, user)

#-----------------------
# zapytanie do bazy o wynik szukania
    def get(self):
        # DropDB()
        zmienna = self.request.get('content')
        user = users.get_current_user()
        querty = db.Query(Object).order('-dates')
        result = querty.fetch(1)

        for results in result:
            zmienna = results.content
            licz = results.licznik
            linkAll = results.lalegro
            linkNok = results.lnokaut
            cenaAll = results.calegro
            cenaNok = results.cnokaut
            imgAll = results.imgalegro
            imgNok = results.imgnokaut

# wyszukanie minimum - najlepszej oferty - nowy Model ------
        if cenaAll < cenaNok:
            cenaMin = cenaAll
            linkMin = linkAll
        else:
            cenaMin = cenaNok
            linkMin = linkNok
#--------------------------------------------------------

        template_values = {
            'user': user,
            'zmienna': zmienna,
            'imgAll': imgAll,
            'linkAll': linkAll,
            'cenaAll': cenaAll,
            'imgNok': imgNok,
            'linkNok': linkNok,
            'cenaNok': cenaNok,
            'cenaMin': cenaMin,
            'linkMin': linkMin,
        }

        doRender(self, 'index_results.html', template_values)


class Statistic(Render):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write('<p>%s</p>' % user)
            # q = Object.all()
            wynik = db.Query(Object).order('-author')
            chat_list = wynik.fetch(limit=100)
            for w in chat_list:
                fraze = w.content
                user = w.author
                data = w.dates

                if w.author == user:
                    # self.response.out.write('<p>szukal: %s -  %s  %s</p>' % (fraze, user, data))
                    # q = Object.all()
                    # wynik = q.filter('author =', aut).order('-dates')
                    today = datetime.today()
                    # limitData.isoformat()
                    limitData2 = datetime(today.year, today.month, today.day-2)
                    if w.dates > limitData2:
                        self.response.out.write('<p>szukal: %s %s %s </p>' % (user, fraze, w.dates))


class PopularObjects(Render):
    def get(self):
        maximum = 0
        maximum2 = 0
        maximum3 = 0
        obiekt = ''
        obiekt2 = ''
        obiekt3 = ''

        query = db.Query(Object).order('-licznik')
        for q in query:
            # self.response.write('<p> maximum1 %s %s</p>' % (obiekt, maximum))
            if q.licznik > 0 and q.licznik > maximum:
                print ".....", q.content, q.licznik
                maximum = q.licznik
                obiekt = q.content
            if q.licznik > 0 and q.licznik > maximum2 and q.content != obiekt:
                print ".....", q.content, q.licznik
                maximum2 = q.licznik
                obiekt2 = q.content
            if q.licznik > 0 and q.licznik > maximum3 and q.content != obiekt and q.content != obiekt2:
                print ".....", q.content, q.licznik
                maximum3 = q.licznik
                obiekt3 = q.content
                #krotnosc = query.filter('author =', aut).order('-dates' )

        #self.response.write('<blockquote>%s time: %s</blockquote>' % (user.content, user.dates))
        if obiekt:
            self.response.write('<p> maximum1 %s %s</p>' % (obiekt, maximum))
        if obiekt2:
            self.response.write('<p> maximum2 %s %s</p>' % (obiekt2, maximum2))
        if obiekt3:
            self.response.write('<p> maximum3 %s %s</p>' % (obiekt3, maximum3))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        doRender(self, 'index.html')


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        # doRender(self, 'loginscreen.html')
        user = users.get_current_user()
        url, url_linktext = Login(self, user)
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            }
        doRender(self, 'login.html', template_values)
#-----------------------------------------


application = webapp2.WSGIApplication([
    ('/results', ResultsPage),
    ('/search', SearchPage),
    #('/results_user', ResultsUserPage),
    ('/createCount/', CreateUser),
    ('/login', LoginHandler),
    ('/index', MainHandler),
    ('/statistic', Statistic),
    ('/popular', PopularObjects),
    ], debug=True)


# def main():
#     application = webapp2.WSGIApplication([

#         ('/results', ResultsPage),
#         ('/search', SearchPage),
#         #('/results_user', ResultsUserPage),
#         ('/createCount/', CreateUser),
#         ('/login', LoginHandler),
#         ('/index', MainHandler),
#         ('/chat', ChatHandler),
#         ('/messages',MesagesHandler),
#         ], debug=True)
#     #wsgiref.handlers.CGIHandler().run(application)

# if __name__=='__main__':
#     main()
