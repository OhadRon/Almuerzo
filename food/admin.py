from models import *
from django.contrib import admin

class PlacesAdmin(admin.ModelAdmin):
	pass

class PersonsAdmin(admin.ModelAdmin):
	pass

class VotesAdmin(admin.ModelAdmin):
	pass
	
class SelectionsAdmin(admin.ModelAdmin):
	pass
	

admin.site.register(Place, PlacesAdmin)
admin.site.register(Person, PersonsAdmin)
admin.site.register(Vote, VotesAdmin)
admin.site.register(Selection, SelectionsAdmin)
