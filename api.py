from flask import Blueprint, render_template, redirect, request, flash, jsonify, make_response
from models import ADDURLPUBLIC, db, User, UrlInfo
from random import choices
from requests import get
from requests.exceptions import ConnectTimeout, ConnectionError
from string import ascii_lowercase, ascii_uppercase
from modules import user_info
from urllib.parse import unquote
from flask_login import login_user, logout_user, current_user

api=Blueprint('api', __name__)

ignore_list=['api', 'login', 'register', 'logout', 'aboutme', 'dashboard', 'urls']

@api.route('/api/AddPublicUrl', methods=['POST'])
def AddPublicUrl():
	if request.method=='POST':
		user_id=current_user.id if current_user.is_authenticated else None
		longurl=unquote(request.form.get('longurl', '', str))
		name=unquote(request.form.get('name', '', str))

	if name=='':
		key=''.join(choices(ascii_lowercase+ascii_uppercase, k=6))
		name=key
	elif len(name)<4:
		return jsonify({'success':False, 'category':'warning', 'message':'Alias/Name should be atleast 4 characters'})
	elif name in ignore_list:
		return jsonify({'success':False, 'category':'warning', 'message':'Alias/Name is already exist!'})
	elif name.isalnum()==False:
		return jsonify({'success':False, 'category':'warning', 'message':'Remove Special Characters from Alias/Name'})
	else:
		find=ADDURLPUBLIC.query.filter_by(shorturl=name).first()
		if find:
			return jsonify({'success':False, 'category':'warning', 'message':'Alias/Name is already exist!'})

	newinfo=ADDURLPUBLIC(longurl=longurl, shorturl=name, user_id=user_id)
	db.session.add(newinfo)
	if current_user.is_authenticated:
		total_url=int(current_user.total_url)+1
		current_user.total_url=total_url
	db.session.commit()
	return jsonify({"success":True, "longurl":longurl, 'category':'success', 'shorturl':request.url_root+name, 'message':'Successfully Shorted your URL. Enjoy!'})


@api.route('/api/register', methods=['POST'])
def register():
	username=unquote(request.form.get('username', '', str))
	email=unquote(request.form.get('email', '', str))
	password=unquote(request.form.get('password', '', str))
	confirm_password=unquote(request.form.get('confirm-password', '', str))
	usercheck=User.query.filter_by(username=username).first()
	emailcheck=User.query.filter_by(email=email).first()
	if len(username)<3:
		return jsonify({'success': False, 'message': 'Username must be atleast 3 characters', 'category':'warning'})
	if not username.isalnum():
		return jsonify({'success': False, 'message': 'Special characters can not used for username', 'category':'warning'})
	elif len(password)<4:
		return jsonify({'success': False, 'message': 'Password must be atleast 4 characters', 'category':'warning'})
	elif password!=confirm_password:
		return jsonify({'success': False, 'message': 'Password & Confirm Password did not matched', 'category':'error'})
	elif usercheck:
		return jsonify({'success': False, 'message': 'Username already exist!', 'category':'error'})
	elif '@' and '.' not in email:
		return jsonify({'success': False, 'message': 'Email Address is not valid', 'category':'error'})
	elif emailcheck:
		return jsonify({'success': False, 'message': 'Email Address already exist!', 'category':'error'})
	new_user=User(username=username, email=email, password=password)
	db.session.add(new_user)
	db.session.commit()

	return jsonify({'success': True, 'message': 'Account Created Successfully', 'category':'success'})

@api.route('/api/login', methods=['POST'])
def login():
	username=unquote(request.form.get('username', '', str))
	password=unquote(request.form.get('password', '', str))	
	remember=(True if request.form.get('checked')=='true' else False)
	if len(username)<3:
		return jsonify({'success': False, 'message': 'Username must be atleast 3 characters', 'category':'warning'})
	elif len(password)<4:
		return jsonify({'success': False, 'message': 'Password must be atleast 4 characters', 'category':'warning'})

	if '@' and '.' in username:
		find_user=User.query.filter_by(email=username).first()
	else:
		find_user=User.query.filter_by(username=username).first()
	if find_user:
		user_pass=find_user.password
		if not password==user_pass:
			return jsonify({'success': False, 'message':'Username/Email or Password are incorrect.', 'category':'error'})
	else:
		return jsonify({'success': False, 'message':'Username/Email or Password are incorrect.', 'category':'error'})
	login_user(find_user)
	return jsonify({'success': True, 'message':'Logined Successfully!', 'category':'success'})

@api.route('/api/deleteurl', methods=['POST'])
def deleteurl():
	url_id=request.form.get('id', type=int)
	if not current_user.is_authenticated:
		return jsonify({'success': False, 'message': 'You are not authenticated', 'category':'error'})
	find=ADDURLPUBLIC.query.get(url_id)
	if not find:
		return jsonify({'success': False, 'message': 'URL does not exist or already deleted', 'category':'warning'})
	user_id=find.user_id
	if not current_user.id==user_id:
		return jsonify({'success': False, 'message': "You Don't own this URL", 'category':'error'})
	info=UrlInfo.query.filter_by(url_id=find.id).all()
	if info:
		for data in info:
			db.session.delete(data)
	total_url=int(current_user.total_url)-1
	current_user.total_url=total_url
	db.session.delete(find)
	db.session.commit()
	return jsonify({'success': True, 'message': "URL Successfully deleted", 'category':'success'})

@api.route('/api/editurl', methods=['POST'])
def editurl():
	url_id=request.form.get('id', type=int)
	longurl=unquote(request.form.get('longurl', '', str))
	name=unquote(request.form.get('name', '', str))
	if not current_user.is_authenticated:
		return jsonify({'success': False, 'message': 'You are not authenticated', 'category':'error'})
	find=ADDURLPUBLIC.query.get(url_id)
	if not find:
		return jsonify({'success': False, 'message': 'URL does not exist or already deleted', 'category':'warning'})
	user_id=find.user_id
	if not current_user.id==user_id:
		return jsonify({'success': False, 'message': "You Do not own this URL", 'category':'error'})
	if name=='':
		key=''.join(choices(ascii_lowercase+ascii_uppercase, k=6))
		name=key
	elif len(name)<4:
		return jsonify({'success':False, 'category':'warning', 'message':'Alias/Name should be atleast 3 characters'})
	elif name in ignore_list:
		return jsonify({'success':False, 'category':'warning', 'message':'Alias/Name is already exist!'})
	elif name.isalnum()==False:
		print(name)
		return jsonify({'success':False, 'category':'warning', 'message':'Remove Special Characters from Alias/Name'})
	else:
		found=ADDURLPUBLIC.query.filter_by(shorturl=name).first()
		if found:
			if not find.shorturl==name:
				return jsonify({'success':False, 'category':'warning', 'message':'Alias/Name is already exist!'})
	find.longurl=longurl
	find.shorturl=name
	db.session.commit()
	return jsonify({'success': True, 'message': "URL Successfully Updated", 'category':'success'})

@api.route('/api/checkip', methods=['POST'])
def checkip():
	ip=request.args.get('ip')
	if not ip:
		return jsonify({'success': False, 'message': 'IP Address not found', 'category':'error'})
	success=False
	while not success:
		try:
			ipinfo=get('http://ip-api.com/json/'+ip).text
			success=True
		except ConnectionError:
			continue
		except ConnectTimeout:
			continue
	# return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{ipinfo}</pre>'
	return ipinfo

@api.route('/api/redirect', methods=['POST'])
def redirect_to_url():
	url=request.form.get('url')
	ipaddress=request.form.get('ip')
	if not url:
		return jsonify({'success': False, 'message': 'URL Not Found', 'category': 'error'})
	if not ipaddress:
		return jsonify({'success': False, 'message': 'URL Not Found', 'category': 'error'})

	find=ADDURLPUBLIC.query.filter_by(shorturl=url).first()
	if find:
		longurl=find.longurl
		id=find.id
		clicks=int(find.clicks)+1
		find.clicks=clicks
		new_visitor=UrlInfo(url_id=id, ip=ipaddress)
		db.session.add(new_visitor)
		db.session.commit()
		return jsonify({'success':True, 'message': 'URL Found', 'category': 'success', 'longurl': longurl})
	else:
		return jsonify({'success': False, 'message': 'URL Not Found', 'category': 'error'})

