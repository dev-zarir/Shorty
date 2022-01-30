from flask import Blueprint, render_template, redirect, request, flash, url_for, jsonify, make_response
from models import ADDURLPUBLIC, db, User, UrlInfo
from flask_login import current_user, login_required
from modules import getip

views=Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@views.route('/iptracker/', methods=['GET', 'POST'])
@views.route('/iptracker', methods=['GET', 'POST'])
def iptracker():
	ipaddress=request.args.get('ip', '', str)
	return render_template('iptracker.html', ipaddress=ipaddress)

@views.route('/dashboard/', methods=['GET', 'POST'])
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	return render_template('dashboard.html')

@views.route('/urls/', methods=['GET', 'POST'])
@views.route('/urls', methods=['GET', 'POST'])
@login_required
def urllist():
	page=request.args.get('page', 1, int)
	per_page=request.args.get('per_page', 5, int)
	user_id=current_user.id
	urls=ADDURLPUBLIC.query.filter_by(user_id=user_id).order_by(ADDURLPUBLIC.time.desc()).paginate(page=page, per_page=per_page)
	return render_template('showurls.html', urls=urls)

@views.route('/urls/<shorturl>/', methods=['GET', 'POST'])
@views.route('/urls/<shorturl>', methods=['GET', 'POST'])
@login_required
def showurlinfo(shorturl):
	page=request.args.get('page', 1, int)
	per_page=request.args.get('per_page', 10, int)
	user_id=current_user.id
	url=ADDURLPUBLIC.query.filter_by(shorturl=shorturl).first()
	if not url:
		return make_response(render_template('404.html'), 404)
	if not url.user_id==user_id:
		return make_response(render_template('404.html'), 404)
	urlinfo=UrlInfo.query.filter_by(url_id=url.id).order_by(UrlInfo.time.desc()).paginate(page=page, per_page=per_page)

	return render_template('showurlinfo.html', url=url, urlinfo=urlinfo)




@views.route('/<url>', methods=['GET', 'POST'])
def redirecttourl(url):
	find=ADDURLPUBLIC.query.filter_by(shorturl=url).first()
	if find:
		return render_template('redirect.html', shorturl=url)
	else:
		return make_response(render_template('404.html'), 404)
	