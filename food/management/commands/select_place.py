from django.core.management.base import BaseCommand, CommandError
from food.models import *
import datetime
from collections import Counter

class Command(BaseCommand):
	help = 'Select the place where we eat today'

	def handle(self, *args, **options):
		today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
		today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

		selection_today = Selection.objects.filter(created__range=(today_min, today_max))

		if len(selection_today) != 0:
			print 'already made a selection today'
		else:
			votes_today = Vote.objects.filter(created__range=(today_min, today_max))

			if len(votes_today) > 0:
				persons_coming = []
				votes = []
				for vote in votes_today:
					persons_coming.append(vote.voter)
					votes.append(vote.place)

				vote_counts = Counter(votes)
				selected_place = max(vote_counts, key=vote_counts.get)
				selection = Selection(place = selected_place)
				selection.save()

				for vote in votes_today:
					if vote.place == selected_place:
						vote.voter.times_won += 1
						vote.voter.save()

				print 'Going to %s, who is coming: %s' % (selected_place, persons_coming)
			else:
				print 'No votes'
