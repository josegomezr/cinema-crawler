[![Build Status](http://drone.josegomezr.me/api/badges/josegomezr/cinema-crawler/status.svg)](http://drone.josegomezr.me/josegomezr/cinema-crawler)

Instalación
===========

Requerimientos
--------------

```bash
apt install -y virtualenv python3 python3-pip python3-setuptools
```

Instala un Virtualenv con Python3
---------------------------------

```bash
virtualenv crawler -p /usr/bin/python3
cd crawler
```

Clona el repo
-------------
```bash
git clone http://git.utils.josegomezr.me/josegomezr/cinema-crawler.git app
cd app
```

Instala dependencias de PyPi (pip)
----------------------------------
```bash
pip install -r requirements.txt
```

Ejecutar
--------

```
python runner.py

```

el archivo `tmp/result.json` contiene el resultado final del crawler.

