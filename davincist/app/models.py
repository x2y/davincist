import random
import time

from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


HOURS_GROWTH_CONSTANT = 1.043
HOURS_MULTIPLIER = 2.0
HOURS_OFFSET = 1.9
TIME_UNIT_MULTIPLIER = 0.4
TIME_UNIT_OFFSET = 0.0
XP_MULTIPLIER = 10.0


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


def randSecret():
  adverbs = [
      'absurdly', 'catastrophically', 'characteristically', 'closely', 'doubtfully', 'dutifully',
      'eerily', 'energetically', 'fantastically', 'firmly', 'fully', 'furtively', 'indubitably',
      'inexplicably', 'inoperably', 'naively', 'paradoxically', 'partially', 'rambunctiously',
      'regretfully', 'romantically', 'simply', 'sporadically', 'stinkily', 'surgically',
      'suspiciously', 'truthfully', 'unquestionably', 'wonderously'
  ]
  adjectives = [
      'bamboozled', 'bemused', 'bifurcated', 'blushing', 'cantankerous', 'cheeky', 'courageous',
      'cuddly', 'fungible', 'gobsmacked', 'greasy', 'groggy', 'grotesque', 'gunky', 'janky',
      'lackadaisical', 'loopy', 'muddy', 'namby-pamby', 'persnickety', 'prickly', 'rapscallion',
      'smelly', 'snarky', 'suspicious', 'wild', 'wonky', 'zealous'
  ]
  nouns = [
      'bazinga', 'bootlegger', 'buccaneer', 'bumfuzzle', 'canoodle', 'carbuncle', 'caterwaul',
      'cattywampus', 'conniption', 'didgeridoo', 'doodle', 'doohickey', 'fiddledeedee', 'girdle',
      'gumbo', 'hornswoggle', 'hullabaloo', 'kahuna', 'katydid', 'kerplunk', 'kinkajou', 'monkey',
      'mugwump', 'noggin', 'pantaloon', 'prestidigitation', 'pickle', 'proctor', 'rumpus',
      'scootch', 'scuttlebutt', 'shebang', 'snuffle', 'spelunker', 'spork', 'sprocket', 'squeegee',
      'tater', 'tuber', 'viper', 'waddle', 'walkabout', 'wasabi', 'weasel', 'whatnot', 'wombat',
      'zeitgeist'
  ]
  adverb = adverbs[random.randint(0, len(adverbs) - 1)]
  adjective = adjectives[random.randint(0, len(adjectives) - 1)]
  noun = nouns[random.randint(0, len(nouns) - 1)]
  article = 'an' if adverb[0] in 'aeiou' else 'a'
  return '%s %s %s %s' % (article, adverb, adjective, noun)


class Track(models.Model):
  name = models.CharField(max_length=64, unique=True, db_index=True)
  description = models.TextField()
  mission = models.CharField(max_length=128)

  @ellipsis(100)
  def __unicode__(self):
    return '%s: %s' % (self.name, self.description)

  class Meta:
    ordering = ['name']


class Level(models.Model):
  name = models.CharField(max_length=64)
  description = models.TextField()
  rank = models.PositiveSmallIntegerField()
  track = models.ForeignKey(Track, related_name='levels')
  is_public = models.BooleanField(default=True)

  def __unicode__(self):
    return '(%s) %d: %s' % (self.track.name, self.rank, self.name)

  @staticmethod
  def hours_needed_in(rank):
    if rank > 0:
      # Round to two decimals for simplicity's sake.
      return round(HOURS_MULTIPLIER * rank ** HOURS_GROWTH_CONSTANT - HOURS_OFFSET, 2)
    else:
      return 0.0

  @staticmethod
  def xp_per_hours_work_in(rank):
    if rank > 0:
      return int(round(XP_MULTIPLIER * rank ** HOURS_GROWTH_CONSTANT))
    else:
      return 0

  @staticmethod
  def cumulative_xp_needed_for(rank):
    xp_needed = 0
    for rank_i in xrange(rank + 1):
      xp_needed += round(Level.hours_needed_in(rank_i) * Level.xp_per_hours_work_in(rank_i))
    return xp_needed

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
    ordering = ['track', 'rank']
    unique_together = (('rank', 'track'), ('name', 'track'))


class Badge(models.Model):
  name = models.CharField(max_length=64)
  level = models.ForeignKey(Level, related_name='badges')
  order = models.FloatField()
  description = models.CharField(max_length=128)
  training = models.TextField()
  challenge = models.CharField(max_length=256)
  BRONZE, SILVER, GOLD, DIAMOND = 1, 2, 4, 6
  GRADES = {BRONZE: 'Bronze',
            SILVER: 'Silver',
            GOLD: 'Gold',
            DIAMOND: 'Diamond'}
  grade = models.SmallIntegerField(choices=GRADES.items(), default=BRONZE)
  is_required = models.BooleanField(default=False)
  requires_verification = models.BooleanField(default=False)

  @ellipsis(100)
  def __unicode__(self):
    return '(%s/%s) %s: %s' % (self.grade, self.level.track.name, self.name,
                               self.description)

  def hours_needed(self):
    if self.level.rank > 0:
      return round(self.grade *
                   (TIME_UNIT_MULTIPLIER * self.level.rank - TIME_UNIT_OFFSET),
                   2)
    else:
      return 0.0

  def xp(self):
    return int(round(self.hours_needed() * Level.xp_per_hours_work_in(self.level.rank)))

  def user_count(self):
    return self.user_tracks.count()

  def track_name(self):
    return self.level.track.name

  class Meta:
    ordering = ['level__track', 'level__rank', 'order']


class Verification(models.Model):
  user = models.ForeignKey(User, related_name='verifications')
  badge = models.ForeignKey(Badge, related_name='verifications')
  verifier = models.ForeignKey(User, related_name='verifications_verified', blank=True, null=True)
  text = models.TextField(blank=True)
  youtube_id = models.SlugField(max_length=11, blank=True)
  UNSUBMITTED, UNVERIFIED, VERIFIED = 'X', 'U', 'V'
  STATUSES = {UNSUBMITTED: 'Unsubmitted',
              UNVERIFIED: 'Unverified',
              VERIFIED: 'Verified'}
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
    get_latest_by = 'timestamp'
    ordering = ['status', 'badge', 'user']
    unique_together = ('user', 'badge')


class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True, related_name='profile')
  MALE, FEMALE, OTHER = 'M', 'F', 'O'
  GENDERS = {MALE: 'Male',
             FEMALE: 'Female',
             OTHER: 'Other'}
  gender = models.CharField(max_length='1', choices=GENDERS.items())

  def xp(self):
    return sum(user_track.xp for user_track in self.user.user_tracks.all())

  def __unicode__(self):
    return '%s profile' % (self.user.username,)


class UserTrack(models.Model):
  user = models.ForeignKey(User, related_name='user_tracks')
  track = models.ForeignKey(Track, related_name='user_tracks')
  level = models.ForeignKey('Level', related_name='user_tracks')
  badges = models.ManyToManyField('Badge', blank=True, related_name='user_tracks')
  xp = models.PositiveIntegerField(default=0)

  def __unicode__(self):
    return '%s/%s' % (self.user, self.track.name)

  def current_challenges(self):
    return (
        self.user.verifications
        .filter(status__in=(Verification.UNSUBMITTED, Verification.UNVERIFIED),
                badge__level__track=self.track)
        .order_by('-timestamp'))

  def next_challenges(self):
    return (
        Badge.objects
        .filter(level=self.level.next())
        .exclude(verifications__user=self.user,
                 verifications__status__in=(Verification.UNSUBMITTED,
                                            Verification.UNVERIFIED,
                                            Verification.VERIFIED))
        .order_by('order'))

  def challenges_to_verify(self):
    return (
        Verification.objects
        .exclude(user=self.user)
        .filter(Q(badge__in=self.badges.all()) |
                Q(badge__level__track=self.track,
                  badge__level__rank__lt=self.level.rank),
                status=Verification.UNVERIFIED)
        .order_by('?'))

  def award_badge(self, verification, verifier):
    # Close the verification.
    verification.status = Verification.VERIFIED
    verification.verifier = verifier
    verification.save()

    # Award the badge and xp.
    self.badges.add(verification.badge)
    self.xp += verification.badge.xp()

    # Award the next level, if available.
    changed_levels = False
    if self.next_challenges().filter(is_required=True).count() == 0:
      next_level = self.level.next()
      if next_level:
        self.level = next_level
        changed_levels = True

    self.save()

    # Send notifications from Prometheus.
    WallPost(user=self.user,
             poster=User.PROMETHEUS,
             text="Congratulations! You've earned the badge \"%s\" in %s." %
                  (verification.badge.name, self.track.name),
             is_public=False,
             verification=verification).save()
    if changed_levels:
      WallPost(user=self.user,
               poster=User.PROMETHEUS,
               text="Congratulations! You've achieved level %d in %s and earned the title \"%s\"." %
                    (self.level.rank, self.track.name, self.level.name),
               is_public=False,
               verification=verification).save()

    return changed_levels

  class Meta:
    ordering = ['user', 'track']
    unique_together = ('user', 'track')


class WallPost(models.Model):
  user = models.ForeignKey(User, related_name='wall_posts')
  poster = models.ForeignKey(User, related_name='wall_posts_posted')
  MAX_TEXT_LENGTH = 512
  text = models.CharField(max_length=MAX_TEXT_LENGTH)
  is_public = models.BooleanField(default=True)
  verification = models.ForeignKey(Verification, related_name='wall_posts', blank=True, null=True)
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
    if self.verification:
      ret['verification'] = self.verification.to_dict()
    return ret

  class Meta:
    get_latest_by = 'timestamp'
    ordering = ['user', '-timestamp']


class Invitation(models.Model):
  email = models.EmailField()
  secret = models.CharField(max_length=75, default=randSecret)
  created = models.DateTimeField(default=datetime.now, editable=False, blank=True)
  emails_sent = models.PositiveSmallIntegerField(default=0)
  last_email_timestamp = models.DateTimeField(blank=True, null=True)
  claimer = models.OneToOneField(User, related_name='invitation', blank=True, null=True)

  def __unicode__(self):
    return '%s: %s - %s' % (self.email, self.secret,
                            datetime.date(self.created).strftime('%b %d, \'%y'))

  class Meta:
    get_latest_by = 'created'
    ordering = ['created']


def user_can_verify(self, verification):
  if not self.is_authenticated():
    return False
  elif self == verification.user:
    return not verification.badge.requires_verification
  elif verification.status != Verification.UNVERIFIED:
    return False
  else:
    try:
      verification_badge = verification.badge
      verification_level = verification_badge.level
      user_track = self.user_tracks.get(track=verification_level.track)
      if user_track.level.rank > verification_level.rank:
        return True
      else:
        return user_track.badges.filter(pk=verification_badge.pk).exists()
    except ObjectDoesNotExist:
      return False


User.add_to_class('can_verify', user_can_verify)


# Monkey-patch the Prometheus User onto the User object for convenience.
User.PROMETHEUS = User.objects.get(pk=7)
