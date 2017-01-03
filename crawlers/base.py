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
    
    handler = logging.FileHandler('./tmp/%s.log' % (self.name), mode='a', encoding='utf8')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s %(args)s')

    handler.setFormatter(formatter)

    self.logger.addHandler(handler)
    self.logger.debug('init')

  def log(self, msg, *args, **kwargs):
    '''@param msg mixed var to log'''
    self.logger.info(msg, *args, **kwargs)

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
    open('./tmp/responses/%s_%s_%i.out' % (self.name, datetime.now().strftime("%Y-%m-%dT%H-%I-%S"), i), 'w').write(str(html_doc))
    self.request_count = self.request_count +1
    return BeautifulSoup(html_doc, 'html.parser')
  
  def doRequest(self, url, **kwargs):
    '''This make an http request and return a 
    @returns requests.Request'''

    self.log('http-request #%(count)d - BEGIN', {
      'url': url,
      **kwargs,
      'count': self.request_count
    })

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
        self.log('http-request #%d - SUCCESS', self.request_count)
        return response
      except (requests.exceptions.ContentDecodingError, requests.exceptions.ConnectionError):
        self.logger.warning('http-request #%d - FAIL, RETRYING (%d times left)', self.request_count, retries)
        retries = retries -1
    raise Exception("Network Error")
