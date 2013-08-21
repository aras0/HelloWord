#!/usr/bin/python
# -*- coding: <encoding name> -*-

import webapp2
import cgi
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db
import modul_13_1 as allegro
import modul_12_3 as nokaut
import ast
import urllib
from datetime import date
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
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    dates = db.DateProperty(auto_now_add=True)
    licznik = db.IntegerProperty()


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
    def get(self):
        user = users.get_current_user()
        url, url_linktext = Login(self, user)
        template_values = {
        'user': user,
        'url': url,
        'url_linktext': url_linktext,
        }
        doRender(self, 'searchPage.html', template_values)
        #self.response.write(MAIN_PAGE_FOOTER_TEMPLATE % (user, url, url_linktext))




class ResultsPage(Render):
    def post(self):
        g = Object()
        zmienna = self.request.get('content')
        user = users.get_current_user()
        url, url_linktext = Login(self, user)

    def get(self):
        #DropDB()
        g = Object()
        zmienna = self.request.get('content')
        user = users.get_current_user()

        url, url_linktext = Login(self, user)


        allegro1 = allegro.loadAlegro(zmienna)
        allegro2 = str(allegro1)
        allegro3 = [item.encode('ascii') for item in ast.literal_eval(allegro2)]

        #self.response.write(allegro3)
        nok = nokaut.downlNokaut(self.request.get('content'), 'a8839b1180ea00fa1cf7c6b74ca01bb5')

        cenaAll = allegro3[0]
        linkAll = allegro3[1]
        imgAll = allegro3[2]

        cenaNok = nok[0]
        Nok = nok[1]
        linkNok = Nok[0]
        imgNok = Nok[1]

        cenaAll = float(cenaAll)
        cenaNok = float(cenaNok)

        if cenaAll < cenaNok:
            cenaMin = cenaAll
            linkMin = linkAll
        else:
            cenaMin = cenaNok
            linkMin = linkNok

        if user:
            aut = user.nickname()
            g.author = aut
            g.content = zmienna

            a = Object.all()
            produkty = a.filter('author =', aut).filter('content =', zmienna).count()
            g.licznik = produkty+1
            print g.licznik
            g.put()

        template_values = {
            'user': user,
            'zmienna': zmienna,
            'allegro3': allegro3,
            'imgAll': imgAll,
            'linkAll': linkAll,
            'cenaAll': cenaAll,
            'imgNok': imgNok,
            'linkNok': linkNok,
            'cenaNok': cenaNok,
            'cenaMin': cenaMin,
            'linkMin': linkMin,
            'url': url,
            'url_linktext': url_linktext,
            'produkty': produkty,

        }

        #self.render_template('mytemplates/index_results.html', template_values=template_values)
        doRender(self, 'index_results.html', template_values)

        if user:
            q = Object.all()
            wynik = q.filter('author =', aut).order('-dates')
            limitData = date.today()
            limitData2 = date(limitData.year, limitData.month, limitData.day-1)
            wynik.filter('dates >', limitData2)
            results = wynik.fetch(5)
            for user in results:
                user.dates
                self.response.write('<blockquote>%s time: %s</blockquote>' % (user.content, user.dates))
                self.response.write('<a href ="%s"> allegro </a>' % linkAll)
                self.response.write('<a href ="%s"> nokaut </a>' % linkNok)
            q2 = Object.all()
            pr = q2.order('content')

            maximum = 0
            maximum2 = 0
            maximum3 = 0
            obiekt = ''
            obiekt2 = ''
            obiekt3 = ''

            query = Object.all()
            for q in query:
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
        # else:
        #     produkty = ""
        #     maximum = ""
        #     maximum2 = ""
        #     maximum3 = ""
        #     obiekt = ""
        #     obiekt2 = ""
        #     obiekt3 = ""

# class MyHandler(webapp2.RequestHandler):
#     def get(self):
#         user = users.get_current_user()
#         if user:
#             greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
#                         (user.nickname(), users.create_logout_url('/')))
#         else:
#             greeting = ('<a href="%s">Sign in or register</a>.' %
#                         users.create_login_url('/'))
#         self.response.out.write('<html><body>%s</body></html>' % greeting)

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
    # def post(self):
    #     acct = self.request.get('account')
    #     pw = self.request.get('password')
    #     logging.info('Checking account=' + acct + ' pw=' + pw)
    #     if pw == '' or acct == '':
    #         doRender(self, 'loginscreen.html', {'error': 'Specify Acct and PW'})
    #     elif pw == 'secret':
    #         doRender(self, 'loggedin.html', {})
    #     else:
    #         doRender(self, 'loginscreen.html', {'error': 'Incorrect password'})





application = webapp2.WSGIApplication([
    ('/results', ResultsPage),
    ('/search', SearchPage),
    #('/results_user', ResultsUserPage),
    ('/createCount/', CreateUser),
    ('/login', LoginHandler),
    ('/index', MainHandler),
    ], debug=True)


# def main():
#     application = webapp2.WSGIApplication([

#         ('/results', ResultsPage),
#         ('/search/', MainPage),
#         ('/results_user', ResultsUserPage),
#         ('/', MyHandler),
#         ], debug=True)
#     wsgiref.handlers.CGIHandler().run(application)

# if __name__=='__main__':
#      main()
