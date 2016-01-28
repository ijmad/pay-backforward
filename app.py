#!/usr/bin/env python

from flask import Flask, redirect, jsonify
app = Flask(__name__)

details = False
complete = False

@app.after_request
def cache_headers(response):    
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  return response

@app.route('/start')
def start():
    global complete, details
    complete = False
    details = False
    return redirect("/details", code=303)

@app.route('/details')
def details_get():
    global complete, details
    if complete:
      return \
        '<html><head><title>Make Payment</title></head>' + \
        '<body>' + \
        '  <h1>GOV.UK Pay</h1>' + \
        '  <p>You already entered your details and paid!</p>' + \
        '  <p><a href="/return">Back to service</a></p>' + \
        '</body>' + \
        '</html>'
    elif details:
      return \
        '<html><head><title>Make Payment</title></head>' + \
        '<body>' + \
        '  <h1>GOV.UK Pay</h1>' + \
        '  <p>You already submitted your details.</p>' + \
        '  <p><a href="/confirm">Confirm</a></p>' + \
        '</body>' + \
        '</html>'
    else:
      return \
        '<html><head><title>Make Payment</title></head>' + \
        '<body>' + \
        '  <h1>GOV.UK Pay</h1>' + \
        '  <form action="/details" method="POST">' + \
        '    <p><input type="text" value="Card Number" size="20" /></p>' + \
        '    <p><button type="submit">Make Payment</button></p></form>' + \
        '  </form>' + \
        '</body>' + \
        '</html>'
    
@app.route('/details', methods=['POST'])
def details_post():
    global details
    details = True
    return redirect("/confirm", code=303)
  
@app.route('/confirm', methods=['GET'])
def confirm_get():
    global complete
    if complete:
      return \
        '<html><head><title>Make Payment</title></head>' + \
        '<body>' + \
        '  <h1>GOV.UK Pay</h1>' + \
        '  <p>You already paid.</p>' + \
        '  <p><a href="/return">Back to service</a></p>' + \
        '</body>' + \
        '</html>'
    else:
      return '<html><head><title>Confirm Payment</title></head>' + \
        '<body>' + \
        '  <h1>GOV.UK Pay</h1>' + \
        '  <form action="/confirm" method="POST">' + \
        '    <p>You really want to pay?</p>' + \
        '    <p><button type="submit">Confirm</button></p>' + \
        '  </form>' + \
        '</body>' + \
        '</html>'
    
@app.route('/confirm', methods=['POST'])
def confirm_post():
  global complete
  complete = True
  return return_redirect()

@app.route('/return', methods=['GET'])
def return_redirect():
  return redirect("http://localhost:5555/return", code=303)

@app.route('/status', methods=['GET'])
def get_status():
  global details, complete
  return jsonify({ 'details': details, 'complete': complete })

if __name__ == '__main__':
    app.run(port=5000, debug=True)