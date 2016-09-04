# EVE-SSO-Python

Web app in Python demonstrating the EVE SSO authentication flow.

## Installing

Download from the server, install the Python prerequisites, and copy and edit the configuration:

```bash
$ git clone https://github.com/Celeo/EVE-SSO-Python.git
$ cd EVE-SSO-Python
$ virtualenv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ cp eve_sso/config.cfg.example eve_sso/config.cfg
```

Edit `eve_sso/config.cfg`, supplying the access string to your database (SQLite works fine) and your EVE third party app information.

```bash
$ export FLASK_APP=eve_sso/app.py
$ flask run
```
