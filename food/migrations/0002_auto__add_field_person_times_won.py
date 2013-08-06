# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.times_won'
        db.add_column(u'food_person', 'times_won',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.times_won'
        db.delete_column(u'food_person', 'times_won')


    models = {
        u'food.person': {
            'Meta': {'object_name': 'Person'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'times_won': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'food.place': {
            'Meta': {'object_name': 'Place'},
            'can_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_sit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_takeaway': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'food.selection': {
            'Meta': {'object_name': 'Selection'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selections'", 'to': u"orm['food.Place']"})
        },
        u'food.vote': {
            'Meta': {'object_name': 'Vote'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['food.Place']"}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['food.Person']"})
        }
    }

    complete_apps = ['food']