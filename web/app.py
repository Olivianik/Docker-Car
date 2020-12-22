import threading

import dash
import dash_bootstrap_components as dbc
from flask import Flask
import locale

from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from MyLogger import logger
from MyPSACC import MyPSACC

app = None
dash_app = None
dispatcher = None


def start_app(title, base_path, debug: bool, host, port):
    global app, dash_app, dispatcher
    try:
        lang = locale.getlocale()[0].split("_")[0]
        locale_url = [f"https://cdn.plot.ly/plotly-locale-{lang}-latest.js"]
    except:
        locale_url = None
        logger.warn("Can't get language")
    app = Flask(__name__)
    app.config["DEBUG"] = debug
    if base_path == "/":
        application = DispatcherMiddleware(app)
        requests_pathname_prefix = None
    else:
        application = DispatcherMiddleware(Flask('dummy_app'), {base_path: app})
        requests_pathname_prefix = base_path + "/"
    dash_app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=locale_url, title=title,
                         server=app, requests_pathname_prefix=requests_pathname_prefix)
    import web.callback
    return run_simple(host, port, application, use_reloader=debug, use_debugger=debug)


myp = None
chc = None


def save_config(my_peugeot: MyPSACC):
    my_peugeot.save_config()
    threading.Timer(30, save_config, args=[my_peugeot]).start()