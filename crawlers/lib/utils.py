# encoding=utf8

import datetime
import re
import unicodedata

re_tag = re.compile(r'\(([^\)]+)\)')
re_nonword = re.compile(r'\W')

meses = [None, "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def cinepolis_today():
  today = datetime.date.today()
  return "%s %s" % (today.day, meses[today.month]) 

def get_meta_from_title(input_str):
  raw_tags = re.findall(re_tag, input_str)
  tags = []
  for tag in raw_tags:
    tags.extend(tag.split('-'))
  for k, tag in enumerate(tags):
    tags[k] = tag
    
  return dict((k, True) for k in tags)

def clean_tags_from_title(input_str):
  return re.sub(re_tag, '', input_str).strip()

def clean_accented_chars(input_str):
  nkfd_form = unicodedata.normalize('NFKD', input_str)
  return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def clean_symbols(input_str):
  return re.sub(re_nonword, '', input_str).strip()

def clean_articles(input_str):
  arts = "el|las|los|un|unos|unas|con|cual".split('|')
  for art in arts:
    input_str = input_str.replace(' '+art+' ', '')
    input_str = input_str.replace(art+' ', '')
    input_str = input_str.replace(' '+art, '')

  return input_str
