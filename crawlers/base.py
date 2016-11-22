from bs4 import BeautifulSoup
import requests
import logging

class BaseCrawler(object):
  '''base class for crawlers'''
  def __init__(self, name):
    '''@param name string crawler name'''
    self.name = name
    self.log('init')

  def log(self, msg):
    '''@param msg mixed var to log'''
    print("LOG[%s]:" % self.name, msg)

  def getTheaters():
    '''This will fetch all theaters for a chain'''
    raise Exception("not implemented yet")
  def getMovies():
    '''This will fetch all movies for each theater'''
    raise Exception("not implemented yet")

  def urlToBS4(self, url, **kwargs):
    '''This make a bs4 object from an http request
    @returns bs4.BeautifulSoup'''
    response = self.doRequest(url, **kwargs).text
    return BeautifulSoup(response, 'html.parser')

  def makeBS4(self, html_doc):
    '''This make a bs4 object from a string
    @returns bs4.BeautifulSoup'''
    return BeautifulSoup(html_doc, 'html.parser')
  
  def doRequest(self, url, **kwargs):
    '''This make an http request and return a 
    @returns requests.Request'''

    self.log('sending-http-request')

    retries = 10 # max retries for http request
    method = kwargs.get('method')
    if method:
      del kwargs['method'] # delete method kwarg so requests doesn't crash
    else:
      method = 'get'

    while retries:
      try:
        if method == 'post':
          response = requests.post(url, **kwargs)
        else:
          response = requests.get(url, **kwargs)

        self.log('successful-http-request')
        return response
      except requests.exceptions.ContentDecodingError:
        self.log('failed-http-request')
        retries = retries -1
    raise Exception("Network Error")
