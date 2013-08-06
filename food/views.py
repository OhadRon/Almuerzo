from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.utils import simplejson
import datetime
from models import *

def home(request,userid=None):
	users = Person.objects.all().order_by('name')

	if userid:
		request.session['userset']=userid
		return logged(request)

	if 'userset' in request.session:
		return logged(request)

	return render(request, 'homepage.html', {'users': users})

def logged(request):

	user = Person.objects.get(id=request.session['userset'])
	now = datetime.datetime.now()

	today_decision_time = now.replace(hour=11, minute=30, second=0, microsecond=0)
	today_afternoon_time = now.replace(hour=14, minute=30, second=0, microsecond=0)

	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
	todays_selection = Selection.objects.filter(created__range=(today_min, today_max))


	if now > today_afternoon_time:
		# end of day
		try:
			place = todays_selection[0].place
			return render(request, 'afternoon.html', {'username': user.name, 'place': place})
		except:
			return render(request, 'afternoon.html', {'username': user.name})
		
	elif len(todays_selection) != 0:
		# What was chosen
		place = todays_selection[0].place
		people = []
		all_votes_today = Vote.objects.filter(created__range=(today_min, today_max))
		for vote in all_votes_today:
			people.append(vote.voter)

		return render(request, 'lunch_chosen.html', {'username': user.name, 'place': place, 'people':people})
	else:
		# vote time
		places = Place.objects.all().order_by('?')

		all_votes_today = Vote.objects.filter(created__range=(today_min, today_max))
		user_vote_today = all_votes_today.filter(voter=user)

		already_voted = len(user_vote_today) != 0

		if already_voted:
			place_voted = user_vote_today[0].place
		else:
			place_voted = None

		return render(request, 'before_lunch.html', {'username': user.name , 'places': places, 'voted': already_voted, 'voted_for':place_voted, 'votes_today': all_votes_today})

	return render(request, 'loggedin.html', {'username': user.name })


def signout(request):
	del request.session['userset']
	return redirect(home)

def chooseplace(request,placeid):
	
	user = Person.objects.get(id=request.session['userset'])

	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
	votes_today = Vote.objects.filter(voter=user, created__range=(today_min, today_max))

	already_voted = len(votes_today) != 0
	place = Place.objects.get(id=placeid)

	if not already_voted:
		vote = Vote(voter=user, place=place)
		vote.save()
	else:
		pass

	return redirect(home)