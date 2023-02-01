# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model as u
from flask_app import DATABASE
from flask_app import bcrypt
# model the class after the user table from our database
from flask import flash #Flash for validations
import re	# the regex module
DATE_SEEN_REGX = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$')

class Magazine:
	def __init__(self, data):
		self.id = data['id']
		self.title = data['title']
		self.description = data['description']
		self.user_id = data['user_id']
		self.subscribers = []
		self.creator = {}
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']	


	@staticmethod
	def validate_magazine(data):
		is_valid = True # we assume this is true
		if len(data['title']) < 2:
			flash("Title must be at least 3 letters.", "err_magazine_title_count")
			is_valid = False
		else:
			potential_magazine = Magazine.get_by_title({'title' :data['title']}) # Match by title
			if potential_magazine:
				if str(potential_magazine.id) != data['id']:# Is edit magazine id different from potential magazine id?
					flash("Title exists and must be unique.", "err_magazine_title_exists")
					is_valid = False
		if len(data['description']) < 10:
			flash("Description must be at least 20 characters.", "err_magazine_description_count")
			is_valid = False

		return is_valid


	# ============ CREATE ==============
	@classmethod
	def create_magazine(cls, data):
		query = """
			INSERT INTO magazines (title,description,user_id)
			VALUES (%(title)s,%(description)s,%(user_id)s);
		"""
		return connectToMySQL(DATABASE).query_db(query, data)
	
	# ============ UPDATE ==============
	@classmethod
	def update(cls, data):
		query = """
			UPDATE magazines
			SET id=%(id)s,title=%(title)s,description= %(description)s
			WHERE id=%(id)s
		"""
		return connectToMySQL(DATABASE).query_db(query, data)
	
	# ============ DELETE ==============
	@classmethod
	def delete(cls, data):
		query = """
			DELETE FROM magazines
			WHERE id=%(id)s
		"""
		return connectToMySQL(DATABASE).query_db(query, data)

	# ========== READ ALL ===============
	@classmethod
	def get_all(cls):
		query = "SELECT * FROM magazines;"
		results = connectToMySQL(DATABASE).query_db(query)
		all_users = [cls(users) for users in results]
		return all_users


	# ========== READ ALL ===============
	@classmethod
	def get_magazine_creator(cls):
		query = """
		SELECT *
		FROM magazines
		LEFT JOIN users ON user_id=users.id;
		"""
		mags = []
		results = connectToMySQL(DATABASE).query_db(query)
		if not results:
			return []
		if results[0]['users.id'] != None:
			for result in results:
				mag = cls( result )
				creator_data = {
					"id" : result["users.id"],
					"fname" : result["fname"],
					"lname" : result["lname"],
					"email" : result["email"],
					"password" : result["password"],
					"created_at" : result["users.created_at"],
					"updated_at" : result["users.updated_at"]
				}
				mag.creator = u.User( creator_data )
				print("\nART\n",vars(mag))
				mags.append(mag)
		return mags


	# ========== READ all ===============
	@classmethod
	def get_all_magazines_users(cls):
		query = """SELECT * 
		FROM magazines
		LEFT JOIN users ON user_id=users.id
		;"""

		results = connectToMySQL(DATABASE).query_db(query)
		print("Resuls  apu---\n",results)
		magazine_reporter = cls( results[0] )
		if results[0]['users.id'] != None:
			for row in results:
				# Now we parse the topping data to make instances of toppings ="keyword from-rainbow">and add them into our list.
				user_data = {
					"id" : row["users.id"],
					"fname" : row["fname"],
					"lname" : row["lname"],
					"email" : row["email"],
					"password" : row["password"], #Hashed
					"created_at" : row["users.created_at"],
					"updated_at" : row["users.updated_at"]
				}
				magazine_reporter.users.append( u.User( user_data ) )
		return magazine_reporter


	# ================READ ALL Many to Many================
	@classmethod
	def get_become_owner( cls , data ):
		query = """SELECT * FROM magazines 
	LEFT JOIN owners ON owners.magazine_id = magazines.id 
	LEFT JOIN users ON owners.user_id = users.id
	WHERE users.id = %(id)s;"""
		results = connectToMySQL(DATABASE).query_db( query , data )
		owner = cls( results[0] )
		if results[0]['users.id'] != None:
			for row in results:
				user_data = {
					"id" : row["users.id"],
					"fname" : row["fname"],
					"lname" : row["lname"],
					"email" : row["email"],
					"password" : row["password"], #Hashed
					"created_at" : row["users.created_at"],
					"updated_at" : row["users.updated_at"]
				}
				owner.owners.append( u.User( user_data ) )
		return owner
	


	@classmethod
	def get_magazine_owners( cls , data ):
		query = """SELECT * FROM magazines 
		LEFT JOIN owners ON owners.magazine_id = magazines.id 
		LEFT JOIN users ON owners.user_id = users.id
		WHERE magazines.id = %(id)s;"""
		results = connectToMySQL(DATABASE).query_db( query , data )
		owner = cls( results[0] )
		if results[0]['users.id'] != None:
			for row in results:
				user_data = {
					"id" : row["users.id"],
					"fname" : row["fname"],
					"lname" : row["lname"],
					"email" : row["email"],
					"password" : row["password"], #Hashed
					"created_at" : row["users.created_at"],
					"updated_at" : row["users.updated_at"]
				}
				owner.owners.append( u.User( user_data ) )
		return owner


	# ========== READ one to one ===============
	@classmethod
	def get_one_magazines_users(cls, data ):
		query = """SELECT * 
		FROM magazines
		LEFT JOIN users ON user_id=users.id
		WHERE magazines.id = %(id)s;
		"""
		results = connectToMySQL(DATABASE).query_db(query,data)
		print("Resuls---opu\n",results)
		magazine_reporter = cls( results[0] )
		if results[0]['users.id'] != None:
			for row in results:
				user_data = {
					"id" : row["users.id"],
					"fname" : row["fname"],
					"lname" : row["lname"],
					"email" : row["email"],
					"password" : row["password"], #Hashed
					"created_at" : row["users.created_at"],
					"updated_at" : row["users.updated_at"]
				}
				magazine_reporter.users.append( u.User( user_data ) )
		return magazine_reporter


	# ========== READ ONE ===============
	@classmethod
	def get_by_title(cls, data):
		query = """
			SELECT *
			FROM magazines
			WHERE title = %(title)s;
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
			FROM magazines
			WHERE magazines.id = %(id)s;
		"""
		results = connectToMySQL(DATABASE).query_db(query, data)
		print(f"The results: {results}")
		if results:
			return cls(results[0])
		return []


	