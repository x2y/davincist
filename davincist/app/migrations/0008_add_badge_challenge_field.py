# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Badge.challenge'
        db.add_column('app_badge', 'challenge',
                      self.gf('django.db.models.fields.CharField')(default='Challenge', max_length=256),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Badge.challenge'
        db.delete_column('app_badge', 'challenge')


    models = {
        'app.badge': {
            'Meta': {'ordering': "['requirement__level__track', 'requirement__level__rank', 'grade', 'name']", 'object_name': 'Badge'},
            'challenge': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'grade': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'requirement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'badges'", 'to': "orm['app.Requirement']"}),
            'requires_verification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'training': ('django.db.models.fields.TextField', [], {})
        },
        'app.level': {
            'Meta': {'ordering': "['track', 'rank']", 'unique_together': "(('rank', 'track'), ('name', 'track'))", 'object_name': 'Level'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'levels'", 'to': "orm['app.Track']"})
        },
        'app.requirement': {
            'Meta': {'ordering': "['level__track', 'level__rank', 'order']", 'unique_together': "(('level', 'order'),)", 'object_name': 'Requirement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requirements'", 'to': "orm['app.Level']"}),
            'order': ('django.db.models.fields.FloatField', [], {})
        },
        'app.track': {
            'Meta': {'ordering': "['name']", 'object_name': 'Track'},
            'backgrounds': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        'app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': "'1'"}),
            'profile_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"})
        },
        'app.usertrack': {
            'Meta': {'ordering': "['user', 'track']", 'unique_together': "(('user', 'track'),)", 'object_name': 'UserTrack'},
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_tracks'", 'blank': 'True', 'to': "orm['app.Badge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_tracks'", 'to': "orm['app.Level']"}),
            'mission': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_tracks'", 'to': "orm['app.Track']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_tracks'", 'to': "orm['auth.User']"}),
            'xp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'app.verification': {
            'Meta': {'ordering': "['status', 'badge', 'user']", 'unique_together': "(('user', 'badge'),)", 'object_name': 'Verification'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'verifications'", 'to': "orm['app.Badge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'verifications'", 'to': "orm['auth.User']"}),
            'verifier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'verifications_verified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'youtube_id': ('django.db.models.fields.SlugField', [], {'max_length': '11', 'blank': 'True'})
        },
        'app.wallpost': {
            'Meta': {'ordering': "['user', '-timestamp']", 'object_name': 'WallPost'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'poster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wall_posts_posted'", 'to': "orm['auth.User']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wall_posts'", 'to': "orm['auth.User']"}),
            'verification': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wall_posts'", 'null': 'True', 'to': "orm['app.Verification']"})
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