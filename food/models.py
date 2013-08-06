from django.db import models

class Place(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=100, unique=True)
	can_order = models.BooleanField(default=False, verbose_name='Can you order from there')
	can_sit = models.BooleanField(default=False, verbose_name='Can you sit there')
	can_takeaway = models.BooleanField(default=False, verbose_name='Can you take to go')

	def __unicode__(self):
		return self.name

class Person(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50,unique=True)
	email = models.EmailField(max_length=120)
	times_won = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class Vote(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	voter = models.ForeignKey('Person', related_name='votes')
	place = models.ForeignKey('Place', related_name='votes')

	def __unicode__(self):
		return self.voter.name + ' | ' + self.place.name + ' | ' + str(self.created)
	
class Selection(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	place = models.ForeignKey('Place', related_name='selections')
	
	def __unicode__(self):
		return self.place.name + ' | ' + str(self.created)