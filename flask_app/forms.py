#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 21:05:27 2021

@author: blazkranjcev
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import InputRequired
import scraper

class ConfigForm(FlaskForm):
    brand_choices = scraper.get_brands()
    brand = SelectField('Znamka', choices = brand_choices, validators=[InputRequired()])
    model = SelectField('Model', choices = [])
    price_min = StringField('Cena od')
    price_max = StringField('Cena do')
    year_min = StringField('Letnik od')
    year_max = StringField('Letnik do')
    km_max = StringField('Prevoženih do')
    fuel = SelectField('Gorivo', choices = ['vsa goriva', 'bencin', 'diesel', 'plin', 'hibridni pogon', 'e-pogon'])
    email = StringField('Email naslov', validators=[InputRequired()])
    submit = SubmitField('Potrdi')
    
                                                                                                                                                                            
    