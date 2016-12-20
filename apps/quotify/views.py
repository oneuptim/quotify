from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Quote, Favorite
# from . import models

def index(request):
    return render(request, 'quotify/index.html')

def register_process(request):
	if request.method == "POST":
		result = User.objects.register(request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['password'], request.POST['confirm_password'], request.POST['dateofbirth'])

		if result[0]==True:
			request.session['id'] = result[1].id
			print result, "*******************************************************"
			# request.session.pop('errors')
			return redirect('/quotes')
		else:

			# request.session['errors'] = result[1]
			messages.add_message(request, messages.WARNING, result[1][0])


			return redirect('/')
	else:

		return redirect ('/')

def login_process(request):
	print "------------ POST ----------------\n", request.POST
	result = User.objects.login(request.POST['email'],request.POST['password'])

	if result[0] == True:
		request.session['id'] = result[1][0].id
		# We have result[1][0] this refers to the results of the query (user query returned) and index of zero which is what we just unwrapped.
		return redirect('/quotes')
	else:
		messages.add_message(request, messages.WARNING, result[1][0])

		# request.session['errors'] = result[1]
		return redirect('/')

def quotes(request):
    if not 'id' in request.session:
        return redirect('/')
    else:
        session = request.session['id']
        loggedInUser = User.objects.get(id=session)
        res = Quote.objects.all().exclude(favoritequote__user__id=session).order_by('-created_at')
        favQuoteList = Favorite.objects.all().order_by('-created_at').filter(user_id=session)
        # quotePoster = Quote.objects.filter(user__id=quoteuser)
        data = {
            'allQuotes': res,
            'favQuotes': favQuoteList,
            'loggedInUser': loggedInUser
            }
        return render(request, 'quotify/quotes.html', data)

def users(request, id):
    if not 'id' in request.session:
        return redirect('/')
    else:
        res = Quote.objects.filter(user_id=id).order_by('-created_at')
        data = {
            'userQuotes': res,
            'quotePoster': res[0].user.first_name,
            'quoteCount': res.count(),
            }
        return render(request, 'quotify/users.html', data)

def add_quote(request):
    if request.method == "POST":
        post = request.POST
        session = request.session['id']
        if not 'id' in request.session:
            return redirect('/')
        else:
            Quote.objects.add_quote(post, session)
            return redirect('/quotes')

def add_fav(request, id):
    session = request.session['id']
    Favorite.objects.add_fav(id, session)
    return redirect('/quotes')

def remove_fav(request, id):
    deleteFav = Favorite.objects.filter(quote_id=id).delete()
    # del (deleteFav)
    print "Deleted", deleteFav, "%"*100
    return redirect('/quotes')

def delete(request, id):
    Quote.objects.get(id=id).delete()
    return redirect('/quotes')

def logout(request):
    del request.session['id']
    return redirect('/')
