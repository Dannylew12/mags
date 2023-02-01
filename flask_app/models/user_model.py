# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import user_model as u
from flask_app import DATABASE
from flask_app import bcrypt
from flask_app.models import magazine_model as m
# model the class after the user table from our database
from flask import flash #Flash for validations
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
USERNAME_REGX = re.compile(r'[a-zA-Z]{2,}')
PASSWORD_REGX = re.compile(r'^[A-Z]{1,}[a-z]{2,}[0-9]{1,}$')

class User:
	def __init__(self, data):
		self.id = data['id']
		self.fname = data['fname']
		self.lname = data['lname']
		self.email = data['email']
		self.password = data['password']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
		self.magazines = []
		self.subscribed = []


	@staticmethod
	def validate_create(data):
		is_valid = True # we assume this is true
		if len(data['fname']) < 3:
			flash("First Name must be at least 3 letters.", "err_user_fname_count")
			is_valid = False
		if not USERNAME_REGX.match(data['fname']):
			flash("First Name, only letters allowed.", "err_user_fname_complexity")
			is_valid = False
		if len(data['lname']) < 3:
			flash("Last Name must be at least 3 characters.", "err_user_lname_count")
			is_valid = False
		if not USERNAME_REGX.match(data['lname']):
			flash("Last Name, only letters allowed.", "err_user_lname_complexity")
			is_valid = False
		if len(data['email']) < 2 or not EMAIL_REGX.match(data['email']):
			flash("Email invalid.", "err_user_email")
			is_valid = False
		else:
			potential_user = User.get_by_email({'email' :data['email']})
			print("User Not Found: ",potential_user )
			if potential_user:
				flash("Email in use.", "err_user_email_exists")
				is_valid = False
		if len(data['password']) < 8:
			flash("Password must be at least 8 characters.", "err_user_password")
			is_valid = False
		if not PASSWORD_REGX.match(data['password']):
			flash("Password is not complex enough.", "err_user_password_complexity")
			is_valid = False
		if data['password-confirm'] != data['password'] :
			flash("Password confirmation does not match.", "err_user_password-confirm")
			is_valid = False
		return is_valid


	@staticmethod
	def validate_user(user,data):
		is_valid = True
		if not EMAIL_REGX.match(data['email']): 
			print(EMAIL_REGX.match(data['email']))
			flash("Invalid Login credentials!", "err_user_login_email")
			is_valid = False
		if len(data['password']) < 3:
			flash("Password must be at least 3 characters.", "err_user_login_password_length")
			is_valid = False
		if not bcrypt.check_password_hash(user.password, data['password']):
			flash("Invalid Login credentials!", "err_user_login_password")
			is_valid = False
		return is_valid


	# ============ CREATE ==============
	@classmethod
	def create_user(cls, data):
		query = """
			INSERT INTO users (fname,lname,email,password)
			VALUES (%(fname)s,%(lname)s,%(email)s,%(password)s);
		"""
		return connectToMySQL(DATABASE).query_db(query, data)
	
	# ============ UPDATE ==============
	@classmethod
	def update_by_id(cls, data):
		query = """
			UPDATE users SET fname=%(fname)s,lname=%(lname)s,email=%(email)s
			WHERE id=%(id)s
		"""
		return connectToMySQL(DATABASE).query_db(query, data)
	
	# ============ DELETE ==============
	@classmethod
	def delete_by_id(cls, data):
		query = """
			DELETE FROM dojos
			WHERE id=%(id)s
		"""
		return connectToMySQL(DATABASE).query_db(query, data)
	

	# ========== READ ALL ===============
	@classmethod
	def get_all_users(cls):
		query = "SELECT * FROM users;"
		all_users = [] # Create an empty list to append our instances of users
		results = connectToMySQL(DATABASE).query_db(query) # make sure to call the connectToMySQL function with the schema you are targeting.
		[all_users.append(cls(users)) for users in results] # Iterate over the db results and create instances of users with cls.
				
		return all_users
	

	# ============ READ ================
	@classmethod
	def get_user_subscriptions( cls , data ):
		query = """SELECT * FROM users
		LEFT JOIN subscribed ON subscribed.user_id = users.id 
		LEFT JOIN magazines ON subscribed.magazine_id = magazines.id
		WHERE users.id = %(id)s;"""
		results = connectToMySQL(DATABASE).query_db( query , data )
		user = cls( results[0] )
		for row_from_db in results:
			magazine_data = {
				"id" : row_from_db["magazines.id"],
				"title" : row_from_db["title"],
				"description" : row_from_db["description"],
				"created_at" : row_from_db["magazines.created_at"],
				"updated_at" : row_from_db["magazines.updated_at"]
			}
			user.magazines.append( m.Magazine( magazine_data ) )
		return user


	# ========== READ ONE ===============
	@classmethod
	def get_by_email(cls, data):
		query = """
			SELECT *
			FROM users
			WHERE email = %(email)s;
		"""
		results = connectToMySQL(DATABASE).query_db(query, data)
		print(f"The results: {results}")
		if results:
			return cls(results[0])
		return []
	
	# ========== READ ONE ===============
	@classmethod
	def get_by_password(cls, data):
		query = """
			SELECT *
			FROM users
			WHERE password = %(password)s;
		"""
		results = connectToMySQL(DATABASE).query_db(query, data)
		print(f"The results: {results}")
		if results:
			return cls(results[0])
		return []
	
	# ========== READ ONE ===============
	@classmethod
	def get_one_by_id(cls, data):
		query = """
			SELECT *
			FROM users
			WHERE id = %(id)s;
		"""
		results = connectToMySQL(DATABASE).query_db(query, data)
		print(f"The results: {results}")
		if results:
			return cls(results[0])
		return []


	# ================READ ALL Many to Many================
	@classmethod
	def get_art_owned( cls , data ):
		query = """SELECT * FROM users
		LEFT JOIN subscribed ON subscribed.user_id = users.id 
		LEFT JOIN magazines ON subscribed.magazine_id = magazines.id
		WHERE users.id = %(id)s;
		"""
		results = connectToMySQL(DATABASE).query_db( query , data )
		print("Owned Art\n",results)
		if results[0]['id'] != None:
			subs = cls( results[0] )
			for row in results:
				mag_data = {
					"id" : row["magazines.id"],
					"title" : row["title"],
					"description" : row["description"],
					"user_id" : row["user_id"],
					"created_at" : row["magazines.created_at"],
					"updated_at" : row["magazines.updated_at"]
				}
				subs.subscribed.append( m.Magazine( mag_data ) )
		return subs


	# ========== READ all ===============
	@classmethod
	def get_all_magazines_user(cls):
		query = """
		SELECT * 
		FROM users
		LEFT JOIN magazines ON user_id=users.id
		ORDER BY magazines.id asc;
		"""

		results = connectToMySQL(DATABASE).query_db(query)
		print("Results--\n",results)
		magazine_reporter = cls( results[0] )
		if results[0]['user_id'] != None:
			for result in results:
				magazine_data = {
					"id" : result["magazines.id"],
					"title" : result["title"],
					"description" : result["description"],
					"created_at" : result["magazines.created_at"],
					"updated_at" : result["magazines.updated_at"],
					"user_id" : result["user_id"],
				}
				magazine_reporter.magazines.append(m.Magazine( magazine_data ))
		return magazine_reporter
	
	# ---------------READ Many to Many-----------------
	@classmethod
	def get_unsubscribed_users(cls):
		query = """
		SELECT *
		FROM users
		WHERE users.id NOT IN (SELECT user_id FROM subscribed);
		"""
		users=[]
		results = connectToMySQL(DATABASE).query_db(query)
		if results:
			for row in results:
				users.append(cls(row))
		return users
	
	# ---------------READ Many to Many-----------------
	@classmethod
	def get_subscribed_users_by_magazine(cls,data):
		query = """
		SELECT *
		FROM users
		LEFT JOIN magazines ON user_id=users.id
		WHERE users.id IN (SELECT user_id FROM subscribed WHERE magazine_id = %(id)s);
		"""
		subs=[]
		results = connectToMySQL(DATABASE).query_db(query,data)
		if results[0]['user_id'] != None:
			subs = cls( results[0] )
			print("results(((((((((((((\n", results)
			for result in results:
				magazine_data = {
					"id" : result["magazines.id"],
					"title" : result["title"],
					"description" : result["description"],
					"created_at" : result["magazines.created_at"],
					"updated_at" : result["magazines.updated_at"],
					"user_id" : result["user_id"],
				}
				subs.subscribed.append(m.Magazine( magazine_data ))
		return subs

	# ---------------READ Many to Many-----------------
	@classmethod
	def get_subscribed_users(cls):
		query = """
		SELECT *
		FROM users
		WHERE users.id IN (SELECT user_id FROM subscribed);
		"""
		users=[]
		results = connectToMySQL(DATABASE).query_db(query)
		if results:
			for row in results:
				users.append(cls(row))
		return users

	# ============= CREATE Subscribed User ==================
	@classmethod
	def create_subscribed_user(cls,data):
		query = """
		INSERT INTO subscribed (user_id,magazine_id)
		VALUES (%(user_id)s,%(magazine_id)s)
		"""
		return connectToMySQL(DATABASE).query_db(query, data)


