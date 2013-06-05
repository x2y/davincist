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


class Track(models.Model):
  name = models.CharField(max_length=64, primary_key=True)
  description = models.TextField()
  mission = models.CharField(max_length=128)
  crest = models.ImageField(upload_to='uploads', null=True)
  # field = models.ForeignKey('Field')
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return '%s: %s' % (self.name, self.description)

  # may be useful, maybe not - commenting out for now. forgot I can't pass parameters in
  def has_user(self):
  #  print "finding user %s" % self.user_tracks.user
    for user_track in self.user_tracks.all():
      if user_track.user.username == "zerogee":
        return True
    return False

  class Meta:
    get_latest_by = 'created'
    ordering = ['name']


class Level(models.Model):
  name = models.CharField(max_length=64)
  description = models.TextField()
  rank = models.PositiveSmallIntegerField()
  track = models.ForeignKey(Track, related_name='levels')
  is_public = models.BooleanField(default=True)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '(%s) %d: %s' % (self.track.name, self.rank, self.name)

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

  def top_10_user_tracks(self):
    return self.user_tracks.order_by('-xp')[:10]

  class Meta:
    get_latest_by = 'created'
    ordering = ['rank']
    unique_together = (('rank', 'track'), ('name', 'track'))


class Quest(models.Model):
  name = models.CharField(max_length=128)
  description = models.TextField()
  level = models.ForeignKey(Level, related_name='quests')
  SMALL, MEDIUM, LARGE, EXTRA_LARGE = 'S', 'M', 'L', 'X'
  SIZES = ((SMALL, 'Small'),
           (MEDIUM, 'Medium'),
           (LARGE, 'Large'),
           (EXTRA_LARGE, 'Extra-large'))
  SIZE_MULTIPLIERS = {SMALL: 1, MEDIUM: 2, LARGE: 4, EXTRA_LARGE: 6}
  size = models.CharField(max_length=1, choices=SIZES, default=SMALL)
  badges = models.ManyToManyField('Badge', blank=True, related_name='quests')
  HONOR, PEER, SENIOR = 'H', 'P', 'S'
  TYPES = ((HONOR, 'Honor'),
           (PEER, 'Peer'),
           (SENIOR, 'Senior'))
  type = models.CharField(max_length=1, choices=TYPES, default=HONOR)
  max_repetitions = models.PositiveSmallIntegerField(default=1)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return '(%s) %s: %s' % (self.level.track.name, self.name, self.description)

  def hours_needed(self):
    if self.level.rank > 0:
      return (self.SIZE_MULTIPLIERS[self.size] *
              (TIME_UNIT_MULTIPLIER * self.level.rank - TIME_UNIT_OFFSET))
    else:
      return 0.0

  def xp(self):
    return round(self.hours_needed() * self.level.xp_per_hours_work())

  class Meta:
    get_latest_by = 'created'
    ordering = ['level', 'name']
    unique_together = ('name', 'level')


class VerificationRequest(models.Model):
  user = models.ForeignKey(User, related_name='verification_requests')
  quest = models.ForeignKey(Quest, related_name='verification_requests')
  text = models.TextField(blank=True)
  youtube_id = models.SlugField(max_length=11, blank=True)
  UNCHECKED, VERIFIED, NOT_VERIFIED = 'U', 'V', 'N'
  STATUSES = ((UNCHECKED, 'Unchecked'),
              (VERIFIED, 'Verified'),
              (NOT_VERIFIED, 'Not verified'))
  status = models.CharField(max_length=1, choices=STATUSES, default=UNCHECKED)
  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '%s for %s - %s' % (self.quest.name, self.user.username, self.status)

  class Meta:
    get_latest_by = 'time'
    ordering = ['status', 'quest', 'user']
    unique_together = ('user', 'quest')


class Verification(models.Model):
  request = models.ForeignKey(VerificationRequest, related_name='verifications')
  verifier = models.ForeignKey(User, related_name='verifications')
  is_positive = models.BooleanField(default=False)
  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '%s for %s - %sverified by %s' % (self.request.quest.name, self.request.user.username,
                                             '' if self.is_positive else 'not ',
                                             self.verifier.username)

  class Meta:
    get_latest_by = 'time'
    ordering = ['verifier', '-timestamp']
    unique_together = ('request', 'verifier')


class Badge(models.Model):
  name = models.CharField(max_length=64)
  description = models.CharField(max_length=128)
  BRONZE, SILVER, GOLD = 1, 2, 3
  GRADES = ((BRONZE, 'Bronze'),
            (SILVER, 'Silver'),
            (GOLD, 'Gold'))
  grade = models.SmallIntegerField(choices=GRADES, default=BRONZE)
  level = models.ForeignKey('Level', related_name='badges')
  # Known type?
  is_required = models.BooleanField(default=False)
  is_public = models.BooleanField(default=True)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return '(%s/%s) %s: %s' % (self.grade, self.level.track.name, self.name, self.description)

  class Meta:
    get_latest_by = 'created'
    ordering = ['level', '-is_required', 'name', 'grade']
    unique_together = ('name', 'grade', 'level')


class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True, related_name='profile')
  MALE, FEMALE, OTHER = 'M', 'F', 'O'
  GENDERS = ((MALE, 'Male'),
             (FEMALE, 'Female'),
             (OTHER, 'Other'))
  gender = models.CharField(max_length='1', choices=GENDERS)
  website = models.URLField(blank=True)
  birth_date = models.DateField()
  bio = models.TextField(blank=True)
  # profile_image = models.ImageField(upload_to='uploads', null=True)

  def xp(self):
    return sum(user_track.xp for user_track in self.user.user_tracks.all())

  def __unicode__(self):
    return '%s profile' % (self.user.username,)


class UserTrack(models.Model):
  user = models.ForeignKey(User, related_name='user_tracks')
  track = models.ForeignKey(Track, related_name='user_tracks')
  mission = models.CharField(max_length=128)
  level = models.ForeignKey('Level', related_name='user_tracks')
  badges = models.ManyToManyField('Badge', blank=True, related_name='user_tracks')
  xp = models.PositiveIntegerField()

  def __unicode__(self):
    return '%s/%s' % (self.user, self.track.name)

  def top_badges(self):
    return self.badges.order_by('-level__rank', '-grade')[:3]

  class Meta:
    ordering = ['user', 'track']
    unique_together = ('user', 'track')


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
