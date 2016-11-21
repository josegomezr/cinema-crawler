import datetime

meses = [None, "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def cinepolis_today():
  today = datetime.date.today()
  return "%s %s" % (today.day, meses[today.month]) 