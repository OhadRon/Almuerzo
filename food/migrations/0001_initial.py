# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Place'
        db.create_table(u'food_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('can_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_sit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_takeaway', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'food', ['Place'])

        # Adding model 'Person'
        db.create_table(u'food_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=120)),
        ))
        db.send_create_signal(u'food', ['Person'])

        # Adding model 'Vote'
        db.create_table(u'food_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['food.Person'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['food.Place'])),
        ))
        db.send_create_signal(u'food', ['Vote'])

        # Adding model 'Selection'
        db.create_table(u'food_selection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['food.Place'])),
        ))
        db.send_create_signal(u'food', ['Selection'])


    def backwards(self, orm):
        # Deleting model 'Place'
        db.delete_table(u'food_place')

        # Deleting model 'Person'
        db.delete_table(u'food_person')

        # Deleting model 'Vote'
        db.delete_table(u'food_vote')

        # Deleting model 'Selection'
        db.delete_table(u'food_selection')


    models = {
        u'food.person': {
            'Meta': {'object_name': 'Person'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
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