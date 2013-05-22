# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field paths on 'UserProfile'
        db.delete_table('app_userprofile_paths')


    def backwards(self, orm):
        # Adding M2M table for field paths on 'UserProfile'
        db.create_table('app_userprofile_paths', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['app.userprofile'], null=False)),
            ('userpath', models.ForeignKey(orm['app.userpath'], null=False))
        ))
        db.create_unique('app_userprofile_paths', ['userprofile_id', 'userpath_id'])


    models = {
        'app.badge': {
            'Meta': {'ordering': "['path', 'name', 'grade']", 'unique_together': "(('name', 'grade', 'path'),)", 'object_name': 'Badge'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'grade': ('django.db.models.fields.CharField', [], {'default': "'B'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'badges'", 'blank': 'True', 'to': "orm['app.Path']"})
        },
        'app.level': {
            'Meta': {'ordering': "['rank']", 'unique_together': "(('rank', 'path'), ('name', 'path'))", 'object_name': 'Level'},
            'badges_needed': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'levels_needing'", 'blank': 'True', 'to': "orm['app.Badge']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'levels'", 'to': "orm['app.Path']"}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'app.path': {
            'Meta': {'ordering': "['name']", 'object_name': 'Path'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'crest': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'mission': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'})
        },
        'app.quest': {
            'Meta': {'ordering': "['level', 'name']", 'unique_together': "(('name', 'path', 'level'),)", 'object_name': 'Quest'},
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'quests'", 'blank': 'True', 'to': "orm['app.Badge']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_peer_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_senior_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quests'", 'to': "orm['app.Level']"}),
            'max_repetitions': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quests'", 'to': "orm['app.Path']"}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'})
        },
        'app.userpath': {
            'Meta': {'ordering': "['user', 'path']", 'unique_together': "(('user', 'path'),)", 'object_name': 'UserPath'},
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_paths'", 'blank': 'True', 'to': "orm['app.Badge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_paths'", 'to': "orm['app.Level']"}),
            'mission': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_paths'", 'to': "orm['app.Path']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_paths'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'xp': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'mission': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']