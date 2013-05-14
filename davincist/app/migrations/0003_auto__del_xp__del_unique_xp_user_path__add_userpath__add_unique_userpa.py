# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Xp', fields ['user', 'path']
        db.delete_unique('app_xp', ['user_id', 'path_id'])

        # Deleting model 'Xp'
        db.delete_table('app_xp')

        # Adding model 'UserPath'
        db.create_table('app_userpath', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('path', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Path'])),
            ('mission', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Level'])),
            ('xp', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('app', ['UserPath'])

        # Adding M2M table for field badges on 'UserPath'
        db.create_table('app_userpath_badges', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userpath', models.ForeignKey(orm['app.userpath'], null=False)),
            ('badge', models.ForeignKey(orm['app.badge'], null=False))
        ))
        db.create_unique('app_userpath_badges', ['userpath_id', 'badge_id'])

        # Adding unique constraint on 'UserPath', fields ['user', 'path']
        db.create_unique('app_userpath', ['user_id', 'path_id'])

        # Removing M2M table for field levels on 'UserProfile'
        db.delete_table('app_userprofile_levels')

        # Removing M2M table for field badges on 'UserProfile'
        db.delete_table('app_userprofile_badges')

        # Adding M2M table for field paths on 'UserProfile'
        db.create_table('app_userprofile_paths', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['app.userprofile'], null=False)),
            ('userpath', models.ForeignKey(orm['app.userpath'], null=False))
        ))
        db.create_unique('app_userprofile_paths', ['userprofile_id', 'userpath_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserPath', fields ['user', 'path']
        db.delete_unique('app_userpath', ['user_id', 'path_id'])

        # Adding model 'Xp'
        db.create_table('app_xp', (
            ('path', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Path'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.UserProfile'])),
        ))
        db.send_create_signal('app', ['Xp'])

        # Adding unique constraint on 'Xp', fields ['user', 'path']
        db.create_unique('app_xp', ['user_id', 'path_id'])

        # Deleting model 'UserPath'
        db.delete_table('app_userpath')

        # Removing M2M table for field badges on 'UserPath'
        db.delete_table('app_userpath_badges')

        # Adding M2M table for field levels on 'UserProfile'
        db.create_table('app_userprofile_levels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['app.userprofile'], null=False)),
            ('level', models.ForeignKey(orm['app.level'], null=False))
        ))
        db.create_unique('app_userprofile_levels', ['userprofile_id', 'level_id'])

        # Adding M2M table for field badges on 'UserProfile'
        db.create_table('app_userprofile_badges', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['app.userprofile'], null=False)),
            ('badge', models.ForeignKey(orm['app.badge'], null=False))
        ))
        db.create_unique('app_userprofile_badges', ['userprofile_id', 'badge_id'])

        # Removing M2M table for field paths on 'UserProfile'
        db.delete_table('app_userprofile_paths')


    models = {
        'app.badge': {
            'Meta': {'ordering': "['path', 'name', 'grade']", 'unique_together': "(('name', 'grade', 'path'),)", 'object_name': 'Badge'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'grade': ('django.db.models.fields.CharField', [], {'default': "'B'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Path']", 'blank': 'True'})
        },
        'app.level': {
            'Meta': {'ordering': "['rank']", 'unique_together': "(('rank', 'path'), ('name', 'path'))", 'object_name': 'Level'},
            'badges_needed': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Badge']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Path']"}),
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
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Badge']", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_peer_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_repeatable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_senior_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Level']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Path']"}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'})
        },
        'app.userpath': {
            'Meta': {'ordering': "['user', 'path']", 'unique_together': "(('user', 'path'),)", 'object_name': 'UserPath'},
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Badge']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Level']"}),
            'mission': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Path']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'xp': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'app.userprofile': {
            'Meta': {'ordering': "['handle']", 'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'mission': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'paths': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.UserPath']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
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