from flask_socketio import SocketIO, send, join_room
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
#import StockPrice as SP
import re
import sqlite3
import pandas as pd
import numpy as np
import requests
import fakereview as fr
import YelpSearch as YS
from flask_table import Table, Col

    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('main.html')


@app.route('/search',methods=['POST'])
def search_page():
	YS.process()
	return render_template('main.html')


@app.route('/main',methods=['POST'])
def main_page():
    	path=request.form['datasetfile']
    	print(path)
    	return render_template('main.html')

@app.route('/countmodel',methods=['POST'])
def count_page():
    	path=request.form['datasetfile']
    	print(path)
    	fr.MainProcessCount(path)
    	return render_template('main.html')
   
@app.route('/tfidfmodel',methods=['POST'])
def tfidf_page():
    	path=request.form['datasetfile']
    	print(path)
    	fr.MainProcessTfidf(path)
    	return render_template('main.html')

@app.route('/ngrammodel',methods=['POST'])
def ngram_page():
    	path=request.form['datasetfile']
    	print(path)
    	fr.MainProcessNgram(path)
    	return render_template('main.html')

# /////////socket io config ///////////////
#when message is recieved from the client    
@socketio.on('message')
def handleMessage(msg):
    print("Message recieved: " + msg)
 
# socket-io error handling
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass


  
  
if __name__ == '__main__':
    socketio.run(app,debug=True,host='127.0.0.1', port=4000)
