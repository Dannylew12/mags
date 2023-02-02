from .. import app, bcrypt  # .. in place of flask_app folder
from flask import render_template,redirect,request,session,flash,url_for

from ..models import user_model as u
from ..models import magazine_model as m



@app.route("/add_magazine")
def add_magazine():
	if(not session['user'] if 'user' in session else False):
		return redirect(url_for('index'))
	return render_template("add_magazine.html", page='Add')



@app.route("/create_magazine", methods=["POST"])
def create_magazine():
	data = {**request.form}
	print(data)
	if not m.Magazine.validate_magazine(data):
		print("not valid", data)
		return redirect(url_for('add_magazine'))
	else:
		print("Creating magazine")
		m.Magazine.create_magazine(data)
		return redirect(url_for('dashboard'))



@app.route("/view_magazine/<int:id>")
def view_magazine(id):
	magazine = m.Magazine.get_one_by_id({'id':id})
	user = u.User.get_one_by_id({'id':magazine.user_id})
	subs = u.User.get_subscribed_users_by_magazine({'id':id})
	return render_template("view_magazine.html", magazine=magazine,
			page='View',user=user, subs=subs)


@app.route("/view_account")
def view_account():
	user = u.User.get_one_by_id({'id':session['id']})
	mags = u.User.get_all_magazines_user()
	subs = u.User.get_subscribed_users()
	return render_template("view_account.html", page='Account',user=user,mags=mags,subs=subs)

@app.route("/update_account", methods=['POST'])
def edit_account():
	print(request.form)
	data = {**request.form,
	'id':session['id']}
	user = u.User.update_by_id(data)
	return redirect(url_for("view_account"))


@app.route('/subscribe', methods=['POST'])
def subscribe():
	print("REQUEST  ",request.form)
	data={
		'user_id': request.form['user_id'],
		'magazine_id':request.form['magazine_id']
	}
	u.User.create_subscribed_user(data)
	return redirect(url_for("view_magazine", id=data['magazine_id']))



@app.route("/edit_magazine/<int:id>")
def edit_magazine(id):
	magazine = m.Magazine.get_one_by_id({'id':id})
	return render_template("edit_magazine.html",art=magazine, page='Edit')



@app.route("/update_magazine/<int:id>", methods=["POST"])
def update_magazine(id):
	data = {**request.form}
	print("************\n",data,"\n***************")
	if not m.Magazine.validate_magazine(data):
		print("not valid save info ", data)
		return redirect(url_for('edit_magazine',id=id))
	else:
		m.Magazine.update(data)
		return redirect(url_for('dashboard'))



@app.route("/delete_magazine/<int:id>", methods=["GET","POST"])
def delete_magazine(id):
	m.Magazine.delete({'id':id})
	return redirect(url_for('dashboard'))