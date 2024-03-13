from flask import (
    Flask, session, redirect, render_template, request, flash, jsonify, send_file, abort
)
import time
from datetime import datetime
import pandas as pd

# Defined in models.py
from models import ModelMgr


# ========================================================
# Flask App
# ========================================================

#app = Flask(__name__, template_folder="./templates", static_folder="./static", static_url_path="")
app = Flask(__name__)

app.secret_key = b'example'

models = ModelMgr()

jpg_map = {
        'coaster' : 'https://images.unsplash.com/photo-1555982105-d25af4182e4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',
        'lens' : 'https://images.unsplash.com/photo-1508423134147-addf71308178?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',
        'chair' : 'https://images.unsplash.com/photo-1449247709967-d4461a6a6103?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',
        'typewriter' : 'https://images.unsplash.com/reserve/LJIZlzHgQ7WPSh5KVTCB_Typewriter.jpg?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',

        'flask' : 'https://images.unsplash.com/photo-1467949576168-6ce8e2df4e13?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',
        'coffee' : 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',
        'top' : 'https://images.unsplash.com/photo-1550837368-6594235de85c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',
        'dice' : 'https://images.unsplash.com/photo-1551431009-a802eeec77b1?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&h=400&q=80',

        'bedding' : 'https://images.unsplash.com/photo-1422190441165-ec2956dc9ecc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',
        'clock' : 'https://images.unsplash.com/photo-1533090161767-e6ffed986c88?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjM0MTM2fQ&auto=format&fit=crop&w=400&h=400&q=80',
        'book' : 'https://images.unsplash.com/photo-1519327232521-1ea2c736d34d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&h=400&q=80',
        }


def init_user_data():
    print('INIT_USER_DATA')

    now = datetime.now()
    userdata = {
        'Administrative' : 0,
        'ProductRelated' : 0,
        'Informational' : 0,
        'Administrative_Duration' : 0,
        'ProductRelated_Duration' : 0,
        'Informational_Duration' : 0,
        'Month' : now.strftime("%b"),
        'Weekend' : now.weekday() > 4,  # 0 is Monday, 6 is Sunday
        }

    return userdata

def increment_userdata_attr(session, attr, amount):
    try:
        print(f'trying to inc {attr}')

        if 'userdata' not in session:
            session['userdata'] = init_user_data()

        session['userdata'][attr] += amount
        session.modified = True  # Mark the session as modified
    except Exception as e:
        print(f"Error incrementing {attr}: {e}")

def start_timer(session, attr):

    now = time.time()

    if 'time_info' in session:
        old_time_info = session['time_info']
        elapsed = now - old_time_info['timestamp']
        prev_type_dur = old_time_info['page_type'] + '_Duration'
        increment_userdata_attr(session, prev_type_dur, elapsed)

    print(f'{attr} TIMER STARTED')

    session['time_info'] = {
            'timestamp' : now,
            'page_type' : attr
            }

def refresh_timer(session):

    now = time.time()

    if 'time_info' in session:
        old_time_info = session['time_info']
        elapsed = now - old_time_info['timestamp']
        prev_type = old_time_info['page_type']
        prev_type_dur = prev_type + '_Duration'
        increment_userdata_attr(session, prev_type_dur, elapsed)

        session['time_info'] = {
                'timestamp' : now,
                'page_type' : prev_type
                }


#######################
##   Dynamic Routes  ##
#######################


@app.route("/usertable")
def usertable():

    print('USERTABLE hit')
    if 'userdata' not in session:
        print('USERTABLE: reset')
        session['userdata'] = init_user_data()

    return render_template('usertable.html', data=session['userdata'])


@app.route('/product')
def product():

    product_name = request.args.get('name', 'Default Product')

    product_image_url = jpg_map[product_name]

    # modify product tracking variables here
    start_timer(session, 'ProductRelated')
    increment_userdata_attr(session, 'ProductRelated', 1)

    return render_template('product.html', product_name=product_name.title(),
                           product_image_url=product_image_url)


@app.route('/leftover-fields', methods=['POST'])
def leftovers():
    # Extracting form data

    leftover_fields = {
            'Browser': int(request.form['Browser']),
            'OperatingSystems': int(request.form['OperatingSystems']),
            'VisitorType': str(request.form['VisitorType']),
            'BounceRates': float(request.form['BounceRates']),
            'ExitRates': float(request.form['ExitRates']),
            'PageValues': float(request.form['PageValues']),
            'SpecialDay': float(request.form['SpecialDay']),
            }

    if 'userdata' not in session:
        session['userdata'] = init_user_data()

    userdata = session['userdata']

    combined_df = models.preproc_userdata(userdata, leftover_fields)
    pred = models.gbdt.predict(combined_df)

    is_revenue_good = (pred[0] == 1)
    return render_template("predict.html", is_revenue_good=is_revenue_good)


@app.route('/reset', methods=['POST'])
def reset():
    if request.method == 'POST':
        session.clear()
        return usertable()

    else:
        return 'Method not allowed', 405


@app.route('/refresh', methods=['POST'])
def refresh():
    if request.method == 'POST':
        refresh_timer(session)
        return usertable()

    else:
        return 'Method not allowed', 405


###################################
##  Routes that modify counters  ##
###################################

@app.route('/sim-shop')
def sim_shop():
    start_timer(session, 'ProductRelated')
    increment_userdata_attr(session, 'ProductRelated', 1)
    return render_template('sim_shop.html')

@app.route("/admin")
def admin():
    start_timer(session, 'Administrative')
    increment_userdata_attr(session, 'Administrative', 1)
    return render_template("admin.html")

@app.route("/about")
def about():
    start_timer(session, 'Informational')
    increment_userdata_attr(session, 'Informational', 1)
    return render_template("about.html")


######################
##   Boring Routes  ##
######################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form_route():
    return render_template("form.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
