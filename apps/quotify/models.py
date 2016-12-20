from __future__ import unicode_literals
from django.db import models
import re, bcrypt

passRegex = re.compile(r'^(?=.{8,15}$)(?=.*[A-Z])(?=.*[0-9]).*$')
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameRegex = re.compile(r'^(?=.{2,})([a-zA-z]*)$')

class UserManager(models.Manager):

	def register(self, first_name, last_name, email, password, confirm_password, dateofbirth):
		errors = []
		if (len(first_name) == 0) or (len(last_name) == 0)  or (len(email) == 0) or (len(password) == 0) or (len(dateofbirth) == 0):
			errors.append("Cannot be blank!")

		if ((not nameRegex.match(first_name)) or (not nameRegex.match(last_name)) ):
		# elif (not emailRegex.match(email)) or (not nameRegex.match(first_name)) or (not nameRegex.match(last_name)):
			errors.append("Name must be at least 2 characters with no letters...")


		if (not emailRegex.match(email)):
			errors.append("Invalid email ....")

		else:

			email_registeres = User.objects.filter(email=email)
			print email_registeres,
			if (email_registeres):
				if (email==email_registeres[0].email):
					errors.append("Email exits in our system ")



		if (not passRegex.match(password)):
			errors.append("Password be at 8-15 characters with one capital letter...")

		if (not (password == confirm_password)):
			errors.append("Password don't match")


		if len(errors) is not 0:
			return (False, errors)
		else:
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			print pw_hash, "888888888888888"
			new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash, dateofbirth=dateofbirth)
			print new_user, "0"*300
		return (True, new_user)

	def login(self, email, password):
		errors =[]

		user = User.objects.filter(email=email)
		# This query returns as an array, should always be unwrapped/unzipped in order to access the objects in the array!

		if user:
			print user,"user exist", user[0].password
			compare_password = password.encode()
			if bcrypt.hashpw(compare_password, user[0].password.encode()) == user[0].password:
			# if (user[0].password == password):
				print user[0].password,"That is your password"

				return (True, user)
			else:
				errors.append("password didnt match")
				print "password didnt match"
				return (False, errors)
		else:
			print "no email found"
			errors.append("No email found in our system, please register dude!!!")
			return (False, errors)

class QuoteManager(models.Manager):
    def add_quote(self, post, session):
		quote = post['quote']
		author = post['author']
		user_id = session

		user = User.objects.get(id=user_id)

		newQuote = Quote.objects.create(quote=quote, author=author, user=user)
        	return(newQuote)

    def add_fav(self, id, session):
		quoteObject = Quote.objects.get(id=id)
		userObject = User.objects.get(id=session)

		newFavObject = Favorite.objects.create(user=userObject, quote=quoteObject)
        	return(newFavObject)

class Quote(models.Model):
    quote = models.CharField(max_length=1000, null=True)
    author = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey('User', related_name = 'quoteuser')
    objects = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey('User', related_name = 'favoriteuser')
    quote = models.ForeignKey('Quote', related_name = 'favoritequote')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

class User(models.Model):
	first_name = models.CharField(max_length=45, blank=True, null=True)
	last_name = models.CharField(max_length=45, blank=True, null=True)
	email = models.EmailField(max_length = 255)
	password = models.CharField(max_length=255)
	dateofbirth = models.DateTimeField(null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()
