#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 20:16:07 2021

@author: blazkranjcev
"""

from flask import Flask, render_template, flash, url_for, redirect, request, jsonify
from forms import ConfigForm
import subprocess
import scraper
import sys
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c20b592005f9e01b3435eb1a472455ba'

@app.route('/', methods=['GET', 'POST'])
def config_form():
    form = ConfigForm()
    # form.model.choices = model_choices
    if form.validate_on_submit():
        flash('Lastnosti avtomobila uspešno vnešene.', 'success')
                                       
    return render_template('main.html', title='Izberi lastnosti', form=form)


@app.route('/model/<brand>')
def car_model(brand):
    model_choices = scraper.get_dropdown_model_options(brand=brand)
    
    modelsArray = []
    
    for model in model_choices:
        modelObj = {}
        modelObj['id'] = model[0]
        modelObj['model'] = model[1]
        modelsArray.append(modelObj)
        
    return jsonify({'models' : modelsArray})
        

@app.route('/car_user_input', methods=['GET', 'POST'])
def car_user_input():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        price_min = request.form['price_min']
        price_max = request.form['price_max']
        year_min = request.form['year_min']
        year_max = request.form['year_max']
        km_max = request.form['km_max']
        fuel = request.form['fuel']
        email_address = request.form['email']
    
    if len(brand.split()) > 1:
        brand.replace(' ', '%20')
        
    if len(model.split()) > 1:
        model.replace(' ', '%20')

    bmw_series_special = ':'
    if 'Serija' in model:
        model = model + bmw_series_special
        
    scraper.main_func(brand, model, price_min, price_max, year_min, year_max, km_max, fuel, email_address)   
    return redirect('/')
# =============================================================================
# @app.route('/background_process_test', methods=['GET', 'POST'])
# def background_process_test():
#     # form = ConfigForm()
#     # model = request.form['model_test']
#     # form_data = request.form
#     # brand = request.form['brand_test']
#     # brand = request.form.get('brand')
#     # test_text = request.form['test_text1']
#     # print(test_text, file=sys.stderr)
#     # brand = request.form['brand']
#     scraper.run_scraper(brand, model)
#     # subprocess.call(['python', 'scraper.py', brand, model])
#     return "some text"
# =============================================================================
    
if __name__ == '__main__':
    app.run(debug=True)