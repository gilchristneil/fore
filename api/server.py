from flask import Flask, request, abort

import smtplib
import ssl
import yaml
import sqlite3

with open("config.yaml", 'r') as yml:
    g.config = yaml.loaf(yml)


app = Flask(__name__)


@app.route('/sharkoutofwater', methods=['POST'])
def sharkoutofwater():
    if request.method == "POST":
        if 'Bear' in request.json['text'] and app.g.config['ma_cache'] == True:
            emitMessage('buy')
            return 'success', 200
        elif 'Bull' in request.json['text'] and app.g.config['ma_cache'] == False:
            emitMessage('sell')
            return 'success', 200
        return 'success', 200
    else:
        abort(400)


@app.route('/masave', methods=['POST'])
def masave():
    if request.method == "POST":
        if 'Average' in request.json['text']:
            if 'Greater' in request.json['text']:
                app.g.config['ma_cache'] = True
            elif 'Less' in request.json['text']:
                app.g.config['ma_cache'] = False
            return 'sucess', 200
        else:
            abort(400)
    else:
        abort(400)


def emitMessage(msg):
    try:
        server = getSmtpServer()
        if msg == 'buy':
            message = """Subject: BUY ALERT FROM FOREX NOTIF

      Price is above 200 moving average and the bearish shark has ended!"""
        if msg == 'sell':
            message = """Subject: SELL ALERT FROM FOREX NOTIF

      Price is below 200 moving average and the bullish shark has ended!"""

        server.sendmail(g.config['smtp']['email'],
                        g.config['smtp']['recipient'], message)
    except Exception as e:
        print(e)


def getSmtpServer():
    if not hasattr(g, 'smtp_server'):
        context = ssl.create_default_context()
        server = smtplib.SMTP(g.config['smtp']['server'], 587)
        server.ehlo()
        server.starttls(context=context)
        server.login(g.config['smtp']['email'], g.config['smtp']['password'])
        g.smtp_server = server
    return g.smtp_server


def getDbCxn():
    if not hasattr(g, 'db_cxn'):
        g.db_cxn = pyodbc.connect('DRIVER='+g.config['sql']['driver']+';SERVER=tcp:'+g.config['sql']['server']+';PORT=1433;DATABASE='+g.config['sql']
                                  ['database']+';UID='+g.config['sql']['username']+';PWD=' + g.config['sql']['password']+';Encrypt=yes;TrustServerCertificate=no')
    return g.db_cxn


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db_cxn'):
        g.db_cxn.close()


def close_smtp(error):
    if hasattr(g, 'smtp_server'):
        g.smtp_server.quit()


if __name__ == '__main__':
    app.run()
