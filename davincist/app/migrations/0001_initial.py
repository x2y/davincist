# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Track'
        db.create_table('app_track', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('mission', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('crest', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('backgrounds', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('app', ['Track'])

        # Adding model 'Level'
        db.create_table('app_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('rank', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(related_name='levels', to=orm['app.Track'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('app', ['Level'])

        # Adding unique constraint on 'Level', fields ['rank', 'track']
        db.create_unique('app_level', ['rank', 'track_id'])

        # Adding unique constraint on 'Level', fields ['name', 'track']
        db.create_unique('app_level', ['name', 'track_id'])

        # Adding model 'Requirement'
        db.create_table('app_requirement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requirements', to=orm['app.Level'])),
            ('order', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('app', ['Requirement'])

        # Adding unique constraint on 'Requirement', fields ['level', 'order']
        db.create_unique('app_requirement', ['level_id', 'order'])

        # Adding model 'Badge'
        db.create_table('app_badge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('requirement', self.gf('django.db.models.fields.related.ForeignKey')(related_name='badges', to=orm['app.Requirement'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('training', self.gf('django.db.models.fields.TextField')()),
            ('grade', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('requires_verification', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('app', ['Badge'])

        # Adding model 'VerificationRequest'
        db.create_table('app_verificationrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='verification_requests', to=orm['auth.User'])),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='verification_requests', to=orm['app.Badge'])),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('youtube_id', self.gf('django.db.models.fields.SlugField')(max_length=11, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='X', max_length=1)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('app', ['VerificationRequest'])

        # Adding unique constraint on 'VerificationRequest', fields ['user', 'badge']
        db.create_unique('app_verificationrequest', ['user_id', 'badge_id'])

        # Adding model 'Verification'
        db.create_table('app_verification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(related_name='verifications', to=orm['app.VerificationRequest'])),
            ('verifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='verifications', to=orm['auth.User'])),
            ('is_positive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('app', ['Verification'])

        # Adding unique constraint on 'Verification', fields ['request', 'verifier']
        db.create_unique('app_verification', ['request_id', 'verifier_id'])

        # Adding model 'UserProfile'
        db.create_table('app_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, primary_key=True, to=orm['auth.User'])),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length='1')),
            ('profile_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal('app', ['UserProfile'])

        # Adding model 'UserTrack'
        db.create_table('app_usertrack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_tracks', to=orm['auth.User'])),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_tracks', to=orm['app.Track'])),
            ('mission', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_tracks', to=orm['app.Level'])),
            ('xp', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('app', ['UserTrack'])

        # Adding unique constraint on 'UserTrack', fields ['user', 'track']
        db.create_unique('app_usertrack', ['user_id', 'track_id'])

        # Adding M2M table for field badges on 'UserTrack'
        db.create_table('app_usertrack_badges', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usertrack', models.ForeignKey(orm['app.usertrack'], null=False)),
            ('badge', models.ForeignKey(orm['app.badge'], null=False))
        ))
        db.create_unique('app_usertrack_badges', ['usertrack_id', 'badge_id'])

        # Adding model 'WallPost'
        db.create_table('app_wallpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wall_posts', to=orm['auth.User'])),
            ('poster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wall_posts_posted', to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('verification_request', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='wall_posts', null=True, to=orm['app.VerificationRequest'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('app', ['WallPost'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserTrack', fields ['user', 'track']
        db.delete_unique('app_usertrack', ['user_id', 'track_id'])

        # Removing unique constraint on 'Verification', fields ['request', 'verifier']
        db.delete_unique('app_verification', ['request_id', 'verifier_id'])

        # Removing unique constraint on 'VerificationRequest', fields ['user', 'badge']
        db.delete_unique('app_verificationrequest', ['user_id', 'badge_id'])

        # Removing unique constraint on 'Requirement', fields ['level', 'order']
        db.delete_unique('app_requirement', ['level_id', 'order'])

        # Removing unique constraint on 'Level', fields ['name', 'track']
        db.delete_unique('app_level', ['name', 'track_id'])

        # Removing unique constraint on 'Level', fields ['rank', 'track']
        db.delete_unique('app_level', ['rank', 'track_id'])

        # Deleting model 'Track'
        db.delete_table('app_track')

        # Deleting model 'Level'
        db.delete_table('app_level')

        # Deleting model 'Requirement'
        db.delete_table('app_requirement')

        # Deleting model 'Badge'
        db.delete_table('app_badge')

        # Deleting model 'VerificationRequest'
        db.delete_table('app_verificationrequest')

        # Deleting model 'Verification'
        db.delete_table('app_verification')

        # Deleting model 'UserProfile'
        db.delete_table('app_userprofile')

        # Deleting model 'UserTrack'
        db.delete_table('app_usertrack')

        # Removing M2M table for field badges on 'UserTrack'
        db.delete_table('app_usertrack_badges')

        # Deleting model 'WallPost'
        db.delete_table('app_wallpost')


    models = {
        'app.badge': {
            'Meta': {'ordering': "['-requirement__level__rank', 'grade', 'name']", 'object_name': 'Badge'},
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
            'Meta': {'ordering': "['rank']", 'unique_together': "(('rank', 'track'), ('name', 'track'))", 'object_name': 'Level'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'levels'", 'to': "orm['app.Track']"})
        },
        'app.requirement': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('level', 'order'),)", 'object_name': 'Requirement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requirements'", 'to': "orm['app.Level']"}),
            'order': ('django.db.models.fields.FloatField', [], {})
        },
        'app.track': {
            'Meta': {'ordering': "['name']", 'object_name': 'Track'},
            'backgrounds': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'crest': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'mission': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'})
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
            'Meta': {'ordering': "['verifier', '-timestamp']", 'unique_together': "(('request', 'verifier'),)", 'object_name': 'Verification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_positive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'verifications'", 'to': "orm['app.VerificationRequest']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'verifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'verifications'", 'to': "orm['auth.User']"})
        },
        'app.verificationrequest': {
            'Meta': {'ordering': "['status', 'badge', 'user']", 'unique_together': "(('user', 'badge'),)", 'object_name': 'VerificationRequest'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'verification_requests'", 'to': "orm['app.Badge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'verification_requests'", 'to': "orm['auth.User']"}),
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
            'verification_request': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wall_posts'", 'null': 'True', 'to': "orm['app.VerificationRequest']"})
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