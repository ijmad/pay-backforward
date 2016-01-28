#!/usr/bin/env python

from flask import Flask, redirect
import requests
app = Flask(__name__)

created = False

@app.after_request
def cache_headers(response):    
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  return response

def get_status():
  r = requests.get('http://localhost:5000/status')
  return r.json()

@app.route('/')
def index():
    global created
    if created:
      status = get_status()
      if status['complete']:
        return redirect('/return', 302)
      elif status['details']:
        return \
          '<html><head><title>Start Payment</title></head>' + \
          '<body>' + \
          '  <h1>Government Service</h1>' + \
          '  <p>You payment is in progress</p>' + \
          '  <p><a href="/start">Resume</a></p>' + \
          '</body>' + \
          '</html>'
      else:
        return \
          '<html><head><title>Start Payment</title></head>' + \
          '<body>' + \
          '  <h1>Government Service</h1>' + \
          '  <p>You started a payment</p>' + \
          '  <p><a href="/start">Resume</a></p>' + \
          '</body>' + \
          '</html>'
    else:
      return \
        '<html><head><title>Start Payment</title></head>' + \
        '<body>' + \
        '  <h1>Government Service</h1>' + \
        '  <p><a href="/start">Start Payment</a></p>' + \
        '</body>' + \
        '</html>'
    
@app.route('/start')
def start():
  global created
  created = True
  return redirect("http://localhost:5000/start", code=302)
  

  
@app.route('/return')
def returned():
    return \
      '<html><head><title>Payment Complete</title></head>' + \
      '<body>' + \
      '  <h1>Government Service</h1>' + \
      '  <p>Payment Complete</p>' + \
      '</body>' + \
      '</html>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)