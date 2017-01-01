import datetime
import re

re_tag = re.compile(r'\(([^\)]+)\)')

meses = [None, "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def cinepolis_today():
  today = datetime.date.today()
  return "%s %s" % (today.day, meses[today.month]) 

def get_meta_from_title(title):
  raw_tags = re.findall(re_tag, title)
  tags = []
  for tag in raw_tags:
    tags.extend(tag.split('-'))
  for k, tag in enumerate(tags):
    tags[k] = tag
    
  return dict((k, True) for k in tags)

def clean_tags_from_title(title):
  return re.sub(re_tag, '', title).strip()
