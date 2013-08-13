import random
import time

from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


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
  backgrounds = models.PositiveSmallIntegerField(default=1)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return '%s: %s' % (self.name, self.description)

  def background_url(self):
    return '%s%s-bkg-%d.jpg' % (settings.STATIC_URL, self.name.lower(),
                                random.randint(0, self.backgrounds - 1))

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

  def user_count(self):
    return self.user_tracks.count()

  def next(self):
    try:
      return self.track.levels.get(rank=self.rank + 1)
    except ObjectDoesNotExist:
      return None

  class Meta:
    get_latest_by = 'created'
    ordering = ['rank']
    unique_together = (('rank', 'track'), ('name', 'track'))


class Requirement(models.Model):
  level = models.ForeignKey(Level, related_name='requirements')
  order = models.FloatField()

  @ellipsis(100)
  def __unicode__(self):
    return '%s (Lvl. %d): %s' % (self.level.track.name, self.level.rank,
                                 ', '.join(badge.name for badge in self.badges.all()))

  class Meta:
    ordering = ['level__rank', 'order']
    unique_together = ('level', 'order')


class Badge(models.Model):
  requirement = models.ForeignKey(Requirement, related_name='badges')
  name = models.CharField(max_length=64)
  description = models.CharField(max_length=128)
  training = models.TextField()
  BRONZE, SILVER, GOLD, DIAMOND = 1, 2, 4, 6
  GRADES = {BRONZE: 'Bronze',
            SILVER: 'Silver',
            GOLD: 'Gold',
            DIAMOND: 'Diamond'}
  grade = models.SmallIntegerField(choices=GRADES.items(), default=BRONZE)
  requires_verification = models.BooleanField(default=False)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return '(%s/%s) %s: %s' % (self.grade, self.requirement.level.track.name, self.name,
                               self.description)

  def hours_needed(self):
    if self.requirement.level.rank > 0:
      return self.grade * (TIME_UNIT_MULTIPLIER * self.requirement.level.rank - TIME_UNIT_OFFSET)
    else:
      return 0.0

  def xp(self):
    return round(self.hours_needed() * self.requirement.level.xp_per_hours_work())

  def user_count(self):
    return self.user_tracks.count()

  def track_name(self):
    return self.requirement.level.track.name

  class Meta:
    get_latest_by = 'created'
    ordering = ['-requirement__level__rank', 'grade', 'name']


class VerificationRequest(models.Model):
  user = models.ForeignKey(User, related_name='verification_requests')
  badge = models.ForeignKey(Badge, related_name='verification_requests')
  text = models.TextField(blank=True)
  youtube_id = models.SlugField(max_length=11, blank=True)
  UNSUBMITTED, UNCHECKED, VERIFIED, NOT_VERIFIED = 'X', 'U', 'V', 'N'
  STATUSES = {UNSUBMITTED: 'Unsubmitted',
              UNCHECKED: 'Unchecked',
              VERIFIED: 'Verified',
              NOT_VERIFIED: 'Not verified'}
  status = models.CharField(max_length=1, choices=STATUSES.items(), default=UNSUBMITTED)
  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '%s for %s - %s' % (self.badge.name, self.user.username, self.status)

  def to_dict(self):
    return {
        'pk': self.pk,
        'user': self.user.username,
        'badge': self.badge.name,
    }

  class Meta:
    get_latest_by = 'time'
    ordering = ['status', 'badge', 'user']
    unique_together = ('user', 'badge')


class Verification(models.Model):
  request = models.ForeignKey(VerificationRequest, related_name='verifications')
  verifier = models.ForeignKey(User, related_name='verifications')
  is_positive = models.BooleanField(default=False)
  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  def __unicode__(self):
    return '%s for %s - %sverified by %s' % (self.request.badge.name, self.request.user.username,
                                             '' if self.is_positive else 'not ',
                                             self.verifier.username)

  class Meta:
    get_latest_by = 'time'
    ordering = ['verifier', '-timestamp']
    unique_together = ('request', 'verifier')


class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True, related_name='profile')
  MALE, FEMALE, OTHER = 'M', 'F', 'O'
  GENDERS = {MALE: 'Male',
             FEMALE: 'Female',
             OTHER: 'Other'}
  gender = models.CharField(max_length='1', choices=GENDERS.items())
  profile_image = models.ImageField(upload_to='uploads', null=True)

  def xp(self):
    return sum(user_track.xp for user_track in self.user.user_tracks.all())

  def __unicode__(self):
    return '%s profile' % (self.user.username,)


class UserTrack(models.Model):
  user = models.ForeignKey(User, related_name='user_tracks')
  track = models.ForeignKey(Track, related_name='user_tracks')
  mission = models.CharField(max_length=128, default='')
  level = models.ForeignKey('Level', related_name='user_tracks')
  badges = models.ManyToManyField('Badge', blank=True, related_name='user_tracks')
  xp = models.PositiveIntegerField(default=0)

  def __unicode__(self):
    return '%s/%s' % (self.user, self.track.name)

  def current_challenges(self):
    return (
        self.user.verification_requests
        .filter(status__in=(VerificationRequest.UNSUBMITTED, VerificationRequest.UNCHECKED),
                badge__requirement__level__track=self.track)
        .order_by('-timestamp'))

  def next_requirements(self):
    return (
        Requirement.objects
        .filter(level=self.level.next())
        .exclude(badges__verification_requests__user=self.user,
                 badges__verification_requests__status__in=(VerificationRequest.UNSUBMITTED,
                                                            VerificationRequest.UNCHECKED,
                                                            VerificationRequest.VERIFIED)))

  def challenges_to_verify(self):
    return (
        VerificationRequest.objects
        .exclude(user=self.user)
        .filter(Q(badge__in=self.badges.all()) |
                Q(badge__requirement__level__track=self.track,
                  badge__requirement__level__rank__lt=self.level.rank),
                status=VerificationRequest.UNCHECKED))

  class Meta:
    ordering = ['user', 'track']
    unique_together = ('user', 'track')


class WallPost(models.Model):
  user = models.ForeignKey(User, related_name='wall_posts')
  poster = models.ForeignKey(User, related_name='wall_posts_posted')
  MAX_TEXT_LENGTH = 512
  text = models.CharField(max_length=MAX_TEXT_LENGTH)
  is_public = models.BooleanField(default=True)
  verification_request = models.ForeignKey(VerificationRequest, related_name='wall_posts',
                                           blank=True, null=True)
  timestamp = models.DateTimeField(default=datetime.now, editable=False, blank=True)

  @ellipsis(100)
  def __unicode__(self):
    return u'@%s: %s \u2014 %s on %s' % (self.user.username, self.text, self.poster.username,
                                         datetime.date(self.timestamp).strftime('%b %d, \'%y'))

  def to_dict(self):
    ret = {
        'pk': self.pk,
        'user': self.user.username,
        'poster': self.poster.username,
        'text': self.text,
        'is_public': self.is_public,
        'timestamp': int(time.mktime(self.timestamp.timetuple())),
    }
    if self.verification_request:
      ret['verification_request'] = self.verification_request.to_dict()
    return ret

  class Meta:
    get_latest_by = 'timestamp'
    ordering = ['user', '-timestamp']
