from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Path(models.Model):
  name = models.CharField(max_length=64, primary_key=True)
  description = models.TextField()
  mission = models.CharField(max_length=128)
  crest = models.ImageField(upload_to='uploads', null=True)
  # field = models.ForeignKey('Field')
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '%s: %s' % (self.name, self.description)

  class Meta:
    get_latest_by = 'created'
    ordering = ['name']


class Level(models.Model):
  name = models.CharField(max_length=64)
  description = models.TextField()
  rank = models.PositiveSmallIntegerField()
  path = models.ForeignKey(Path)
  badges_needed = models.ManyToManyField('Badge')
  is_public = models.BooleanField(default=True)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '(%s) %d: %s' % (self.path.name, self.rank, self.name)

  def xp_needed(self):
    return 20 ** self.rank

  class Meta:
    get_latest_by = 'created'
    ordering = ['rank']
    unique_together = (('rank', 'path'), ('name', 'path'))


class Quest(models.Model):
  name = models.CharField(max_length=128)
  description = models.TextField()
  path = models.ForeignKey(Path)
  level = models.ForeignKey(Level)
  SMALL, MEDIUM, LARGE, EXTRA_LARGE = 'S', 'M', 'L', 'X'
  QUEST_SIZES = ((SMALL, 'Small'),
                 (MEDIUM, 'Medium'),
                 (LARGE, 'Large'),
                 (EXTRA_LARGE, 'Extra-large'))
  QUEST_SIZE_MULTIPLIERS = {SMALL: 1, MEDIUM: 2, LARGE: 3, EXTRA_LARGE:5}
  size = models.CharField(max_length=1, choices=QUEST_SIZES, default=SMALL)
  badge = models.ForeignKey('Badge', blank=True)
  is_repeatable = models.BooleanField(default=False) # change to max reps
  is_peer_validated = models.BooleanField(default=False)
  is_senior_validated = models.BooleanField(default=False)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '(%s) %s: %s' % (self.path.name, self.name, self.description)

  def xp(self):
    return self.QUEST_SIZE_MULTIPLIERS[self.size] ** self.level.rank

  class Meta:
    get_latest_by = 'created'
    ordering = ['level', 'name']
    unique_together = ('name', 'path', 'level')


class Badge(models.Model):
  name = models.CharField(max_length=64)
  description = models.CharField(max_length=128)
  BRONZE, SILVER, GOLD = 'B', 'S', 'G'
  BADGE_GRADES = ((BRONZE, 'Bronze'),
                  (SILVER, 'Silver'),
                  (GOLD, 'Gold'))
  grade = models.CharField(max_length='1', choices=BADGE_GRADES, default=BRONZE)
  path = models.ForeignKey('Path', blank=True)
  # Known type?
  is_public = models.BooleanField(default=True)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '(%s/%s) %s: %s' % (self.grade, self.path.name, self.name, self.description)

  class Meta:
    get_latest_by = 'created'
    ordering = ['path', 'name', 'grade']
    unique_together = ('name', 'grade', 'path')


class Xp(models.Model):
  user = models.ForeignKey('UserProfile')
  path = models.ForeignKey('Path')
  value = models.PositiveIntegerField()

  def __unicode__(self):
    return '%s: %d' % (self.path.name, self.value)

  class Meta:
    ordering = ['user', '-value', 'path']
    unique_together = ('user', 'path')


class UserProfile(models.Model):
  handle = models.CharField(max_length=32, primary_key=True)
  user = models.ForeignKey(User, unique=True)
  first_name = models.CharField(max_length=32)
  last_name = models.CharField(max_length=32)
  website = models.URLField(blank=True)
  email = models.EmailField()
  birth_date = models.DateField()
  bio = models.TextField()
  # profile_image = models.ImageField(upload_to='uploads', null=True)
  mission = models.CharField(max_length=128)
  levels = models.ManyToManyField('Level', blank=True)
  badges = models.ManyToManyField('Badge', blank=True)
  last_seen = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '%s' % (self.handle,)

  class Meta:
    ordering = ['handle']


# class LevelEvent(models.Model):
#  user = models.ForeignKey('User')
#  level = models.ForeignKey('Level')
#  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)
#
#  def __unicode__(self):
#    return '%s to %s on %s' % (self.user.handle, str(self.level), str(self.timestamp))
#
#  class Meta:
#    ordering = ['user', 'timestamp']
#    get_latest_by = 'timestamp'
#
#
# class QuestEvent(models.Model):
#  user = models.ForeignKey('User')
#  quest = models.ForeignKey('Quest')
#  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)
#
#  def __unicode__(self):
#    return '%s completed %s on %s' % (self.user.handle, str(self.quest), str(self.timestamp))
#
#  class Meta:
#    ordering = ['user', 'timestamp']
#    get_latest_by = 'timestamp'
#
#
# class BadgeEvent(models.Model):
#  user = models.ForeignKey('User')
#  badge = models.ForeignKey('Badge')
#  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)
#
#  def __unicode__(self):
#    return '%s received %s on %s' % (self.user.handle, str(self.badge), str(self.timestamp))
#
#  class Meta:
#    ordering = ['user', 'timestamp']
#    get_latest_by = 'timestamp'
#
#
# class XpEvent(models.Model):
#  user = models.ForeignKey('User')
#  path = models.ForeignKey('Path')
#  xp = models.PositiveIntegerField()
#  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)
#
#  def __unicode__(self):
#    return '%s received %d XP in %s on %s' % (self.user.handle, self.xp, self.path.name,
#                                              str(self.timestamp))
#
#  class Meta:
#    ordering = ['user', 'path', 'timestamp']
#    get_latest_by = 'timestamp'


# Chat
# Forum
# Gallery
# Moderation
# Flagging
# 1:1 Mail
# Wall
# Achievements?
# Stats
# Meta
# Teams
# Path-specific mission
