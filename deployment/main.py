"""
DeepSkin API

This Script implements a Flask-based sever for our DeepSkin project. It provides frontend for users interaction as well as entries for querying the API.


"""


###### Import Section ######

import numpy as np 
import pathlib
import time
import os
import requests


from flask import Flask, render_template, request, jsonify
from models.predict import load_model, predict
from waitress import serve

##### Web Server 

HOST = "0.0.0.0"
PORT = 80



# Start WebServer

app = Flask(__name__)








###### API #####



@app.route("/")
def submit():
    """
    First Test of the API

    """
    return render_template("welcome.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)
