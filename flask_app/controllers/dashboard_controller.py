from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash,url_for,make_response

from flask_app.models import user_model as u
from flask_app.models import magazine_model as m

def cache_control(mags, page):
	response = make_response(render_template("dashboard.html",mags=mags, page=page))
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response	

# ,arts=arts, art_owned=art_owned, page=page   arts, art_owned, page

@app.route("/dashboard")
def dashboard():
	if 'user' not in session:
		response = make_response(render_template("index.html", page='Index'))
		response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
		return response
	else:
		print("Dashboard user in session ",session)
		mags = m.Magazine.get_magazine_creator()

		return cache_control(mags, page='Dashboard')



@app.route("/login", methods=["POST"])
def login():
	if(session['user'] if 'user' in session else False):
		print("Login user in session ",session)
		return redirect(url_for('index'))
	else:
		print('No session')
		redirect(url_for('index'))
	data = {**request.form}
	print("data\n", data)
	user = u.User.get_by_email(data)
	if not user:
		return redirect(url_for('index'))

	if not u.User.validate_user(user,data):
		return redirect(url_for('index'))
	
	print(bcrypt.check_password_hash(user.password, data['password']))
	if bcrypt.check_password_hash(user.password, data['password']):
		session['user'] = user.email
		session['id'] = user.id
		print("Session info",session,session['id'])

	return redirect(url_for('dashboard'))



@app.route("/logout")
def logout():
	session.clear()
	session["__invalidate__"] = True
	print("session destroyed")
	return redirect(url_for('index'))

@app.after_request
def remove_if_invalid(response):
	if "__invalidate__" in session:
		response.delete_cookie(app.session_cookie_name)
		print("Cookie deleted.")
	return response


@app.route("/create", methods=["POST"])
def create_user():
	data = {**request.form}

	if not u.User.validate_create(data):
		print("not valid", data)
		return redirect(url_for('index'))
	else:
		data['password'] = bcrypt.generate_password_hash(data['password'])
		u.User.create_user(data)
		return redirect(url_for('index'))
