from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


HOURS_GROWTH_CONSTANT = 2.2
HOURS_MULTIPLIER = 2.04
HOURS_OFFSET = 1.04
TIME_UNIT_MULTIPLIER = 1.25
TIME_UNIT_OFFSET = 1.0
XP_MULTIPLIER = 20


def ellipsis(width):
  def _decorator(function):
    def _wrapper(*args, **kwargs):
      text = function(*args, **kwargs)
      if len(text) > width:
        return text[:width - 3] + '...'
      else:
        return text
    return _wrapper
  return _decorator


class Path(models.Model):
  name = models.CharField(max_length=64, primary_key=True)
  description = models.TextField()
  mission = models.CharField(max_length=128)
  crest = models.ImageField(upload_to='uploads', null=True)
  # field = models.ForeignKey('Field')
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return '%s: %s' % (self.name, self.description)

  class Meta:
    get_latest_by = 'created'
    ordering = ['name']


class Level(models.Model):
  name = models.CharField(max_length=64)
  description = models.TextField()
  rank = models.PositiveSmallIntegerField()
  path = models.ForeignKey(Path, related_name='levels')
  is_public = models.BooleanField(default=True)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '(%s) %d: %s' % (self.path.name, self.rank, self.name)

  def hours_needed(self):
    if self.rank > 0:
      return round(HOURS_MULTIPLIER * self.rank ** HOURS_GROWTH_CONSTANT - HOURS_OFFSET)
    else:
      return 0.0

  def xp_per_hours_work(self):
    if self.rank > 0:
      return round(XP_MULTIPLIER * self.rank ** HOURS_GROWTH_CONSTANT)
    else:
      return 0.0

  def xp_needed(self):
    return self.hours_needed() * self.xp_per_hours_work()
    
  def top_10_users(self):
    return self.user_paths.order_by('-xp')[:10]

  class Meta:
    get_latest_by = 'created'
    ordering = ['rank']
    unique_together = (('rank', 'path'), ('name', 'path'))


class Quest(models.Model):
  name = models.CharField(max_length=128)
  description = models.TextField()
  path = models.ForeignKey(Path, related_name='quests')
  level = models.ForeignKey(Level, related_name='quests')
  SMALL, MEDIUM, LARGE, EXTRA_LARGE = 'S', 'M', 'L', 'X'
  QUEST_SIZES = ((SMALL, 'Small'),
                 (MEDIUM, 'Medium'),
                 (LARGE, 'Large'),
                 (EXTRA_LARGE, 'Extra-large'))
  QUEST_SIZE_MULTIPLIERS = {SMALL: 1, MEDIUM: 2, LARGE: 4, EXTRA_LARGE: 6}
  size = models.CharField(max_length=1, choices=QUEST_SIZES, default=SMALL)
  badges = models.ManyToManyField('Badge', blank=True, related_name='quests')
  max_repetitions = models.PositiveSmallIntegerField(default=1)
  is_peer_validated = models.BooleanField(default=False)
  is_senior_validated = models.BooleanField(default=False)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return '(%s) %s: %s' % (self.path.name, self.name, self.description)

  def hours_needed(self):
    if self.level.rank > 0:
      return (self.QUEST_SIZE_MULTIPLIERS[self.size] *
          (TIME_UNIT_MULTIPLIER * self.level.rank - TIME_UNIT_OFFSET))
    else:
      return 0.0

  def xp(self):
    return round(self.hours_needed() * self.level.xp_per_hours_work())

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
  level = models.ForeignKey('Level', related_name='badges')
  # Known type?
  is_public = models.BooleanField(default=True)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return '(%s/%s) %s: %s' % (self.grade, self.level.path.name, self.name, self.description)

  class Meta:
    get_latest_by = 'created'
    ordering = ['level', 'name', 'grade']
    unique_together = ('name', 'grade', 'level')


class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True, related_name='profile')
  website = models.URLField(blank=True)
  birth_date = models.DateField()
  bio = models.TextField()
  # profile_image = models.ImageField(upload_to='uploads', null=True)
  mission = models.CharField(max_length=128)

  def __unicode__(self):
    return '%s profile' % (self.user.username,)


class UserPath(models.Model):
  user = models.ForeignKey(User, related_name='user_paths')
  path = models.ForeignKey('Path', related_name='user_paths')
  mission = models.CharField(max_length=128)
  level = models.ForeignKey('Level', related_name='user_paths')
  badges = models.ManyToManyField('Badge', blank=True, related_name='user_paths')
  xp = models.PositiveIntegerField()

  def __unicode__(self):
    return '%s/%s' % (self.user, self.path.name)

  class Meta:
    ordering = ['user', 'path']
    unique_together = ('user', 'path')


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
