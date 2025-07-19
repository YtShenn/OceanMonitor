import sys,os
from flask import Flask, render_template, request, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import click
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    role = db.Column(db.String(24), nullable=False)
    analysis_id=db.Column(db.Integer)
    update_id=db.Column(db.Integer)

    def __init__(self, username, password,role,analysis_id,update_id):
        self.username = username
        self.password = password
        self.role = role
        self.analysis_id=analysis_id
        self.update_id=update_id

class Location(db.Model, UserMixin):
    loc_id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)

    def __init__(self, loc_id, lon, lat):
        self.loc_id = loc_id
        self.lon = lon
        self.lat = lat

class Ocean_Info(db.Model, UserMixin):
    info_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    sea_level = db.Column(db.Float, nullable=False)

    def __init__(self, info_id, time, temperature, sea_level):
        self.info_id = info_id
        self.time = time
        self.temperature = temperature
        self.sea_level = sea_level

class Update_record(db.Model, UserMixin):
    ud_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date, nullable=False)
    info_id = db.Column(db.Integer, nullable=False)

    def __init__(self, info_id, time, ud_id):
        self.info_id = info_id
        self.time = time
        self.ud_id = ud_id

class Report(db.Model, UserMixin):
    report_id = db.Column(db.Integer, primary_key=True)
    var_tmp = db.Column(db.Float, nullable=False)
    var_level = db.Column(db.Float, nullable=False)
    pred_tmp = db.Column(db.Float, nullable=False)
    pred_level = db.Column(db.Float, nullable=False)

    def __init__(self, report_id, var_tmp, var_level, pred_tmp, pred_level):
        self.report_id = report_id
        self.var_tmp = var_tmp
        self.var_level = var_level
        self.pred_tmp = pred_tmp
        self.pred_level = pred_level