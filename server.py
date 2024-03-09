from flask import (
    Flask, redirect, render_template, request, flash, jsonify, send_file, abort
)
import os
import pandas as pd
import csv
import pickle


# ========================================================
# Flask App
# ========================================================

#app = Flask(__name__, template_folder="./templates", static_folder="./static", static_url_path="")
app = Flask(__name__)

# app.secret_key = b'hypermedia rocks'

@app.route("/product")
def product():
    # modify product tracking variables here
    return render_template("product.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form_route():
    return render_template("form.html")

@app.route('/sim-shop')
def sim_shop():
    return render_template('sim_shop.html')

@app.route("/search")
def search():
    results_list=[]
    q = request.args.get("q") # ?q=
    if q is not None:
        return render_template("index.html")
    return render_template("search.html", results=results_list)

if __name__ == "__main__":
    app.run(port=5001, debug=True)


