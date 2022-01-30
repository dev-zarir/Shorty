from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import request
from modules import user_info
from datetime import datetime
from modules import getip

db=SQLAlchemy()

class ADDURLPUBLIC(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	longurl=db.Column(db.String(200), nullable=False)
	shorturl=db.Column(db.String(200), nullable=False)
	time=db.Column(db.String(200), nullable=False)
	ip=db.Column(db.String(200), nullable=False)
	clicks=db.Column(db.Integer)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
	urlinfo=db.relationship('UrlInfo')

	def __init__(self, longurl, shorturl, user_id=None, clicks=0):
		self.longurl=longurl
		self.shorturl=shorturl
		self.clicks=clicks
		self.ip=getip()
		self.time=str(datetime.now())[:-7]
		self.user_id=user_id

class UrlInfo(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	url_id=db.Column(db.Integer, db.ForeignKey('ADDURLPUBLIC.id'))
	ip=db.Column(db.String(200), nullable=False)
	time=db.Column(db.String(200), nullable=False)

	def __init__(self, url_id, ip='None'):
		self.url_id=url_id
		self.ip=ip
		self.time=str(datetime.now())[:-7]

class User(db.Model, UserMixin):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(200), nullable=False)
	email=db.Column(db.String(200), nullable=False)
	password=db.Column(db.String(200), nullable=False)
	time=db.Column(db.String(200), nullable=False)
	ip=db.Column(db.String(200), nullable=False)
	total_url=db.Column(db.Integer)
	urls=db.relationship('ADDURLPUBLIC')

	def __init__(self, username, email, password, total_url=0):
		self.username=username
		self.email=email
		self.password=password
		self.total_url=total_url
		self.ip=getip()
		self.time=str(datetime.now())[:-7]
