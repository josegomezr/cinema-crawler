# encoding=utf8
from bs4 import BeautifulSoup
import requests
import logging
from datetime import datetime

class BaseCrawler(object):
  '''base class for crawlers'''
  def __init__(self, name):
    '''@param name string crawler name'''
    self.name = name
    self.request_count = 1
    self.logger = logging.getLogger(self.name)
    self.logger.setLevel(logging.DEBUG)
    self.logger.addHandler(logging.FileHandler('./tmp/log-%s.log' % (self.name), mode='a', encoding='utf8'))
    self.logger.debug('init')

  def log(self, msg):
    '''@param msg mixed var to log'''
    self.logger.info(msg)

  def getTheaters():
    '''This will fetch all theaters for a chain'''
    raise Exception("not implemented yet")
  def getMovies():
    '''This will fetch all movies for each theater'''
    raise Exception("not implemented yet")

  def urlToBS4(self, url, **kwargs):
    '''This make a bs4 object from an http request
    @returns bs4.BeautifulSoup'''
    response = self.doRequest(url, **kwargs)
    return self.makeBS4(response.text)

  def makeBS4(self, html_doc):
    '''This make a bs4 object from a string
    @returns bs4.BeautifulSoup'''
    i = self.request_count
    open('./tmp/%s_%s_%i.request' % (self.name, datetime.now().strftime("%Y-%m-%dT%H-%I-%S"), i), 'w').write(str(html_doc))
    self.request_count = self.request_count +1
    return BeautifulSoup(html_doc, 'html.parser')
  
  def doRequest(self, url, **kwargs):
    '''This make an http request and return a 
    @returns requests.Request'''

    self.log('sending-http-request #[%d]\nURL:%s\nARGS:%s\n' % (self.request_count, url, str(kwargs)))

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
      except (requests.exceptions.ContentDecodingError, requests.exceptions.ConnectionError):
        self.log('failed-http-request retrying')
        retries = retries -1
    raise Exception("Network Error")
