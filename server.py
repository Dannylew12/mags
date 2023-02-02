from flask_app import app, bcrypt
from functools import wraps
from flask_app.controllers import dashboard_controller # Import controllers for routing
from flask_app.controllers import magazine_controller

from flask import render_template,redirect,request,session,flash,url_for,make_response

from flask_app.models import user_model as u

# def cache_control(f):
# 	@wraps(f)
# 	def decorated_function():
# 		users = f()
# 		response = make_response(render_template("index.html",users=users, page='Index'))
# 		response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
# 		return response
# 	return decorated_function

def cache_control(u):
	response = make_response(render_template("index.html",users=u, page='Index'))
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response	


@app.route("/")
def index():
	if 'user' in session:
		return redirect(url_for('dashboard'))
	else:
		print('No session @ Index')
	users=u.User.get_all_users()

	return cache_control(users)


if __name__ == "__main__":
	app.run(debug=True, port=5000)