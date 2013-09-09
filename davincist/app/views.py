from annoying.decorators import ajax_request, render_to
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import *
from models import *
from validators import *


WALL_POSTS_PER_PAGE = 15


# Attributes will be defined outside init pylint: disable=W0201
class Response(object):
  @classmethod
  def errors(cls, *errors):
    if len(errors) == 1 and hasattr(errors[0], '__iter__'):
      return {'errors': errors[0]}
    else:
      return {'errors': errors}


def get_user_track(request, track_name):
  if request.user.is_authenticated():
    try:
      return request.user.user_tracks.get(track__name=track_name)
    except ObjectDoesNotExist:
      pass
  return None


@render_to('home.html')
def home(request):
  r = Response()
  r.tracks = Track.objects.all()
  return r.__dict__


@render_to('about.html')
def about(request):
  r = Response()
  return r.__dict__


@render_to('track_list.html')
def track_list(request):
  r = Response()
  r.tracks = Track.objects.all()
  return r.__dict__


@render_to('track_detail.html')
def track_detail(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  r.user_track = get_user_track(request, track_name)
  return r.__dict__


@render_to('track_users.html')
def track_users(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  r.user_track = get_user_track(request, track_name)
  return r.__dict__


@render_to('track_levels.html')
def track_levels(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  r.user_track = get_user_track(request, track_name)
  return r.__dict__


@render_to('track_badges.html')
def track_badges(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  r.user_track = get_user_track(request, track_name)
  return r.__dict__


@render_to('badge_detail.html')
def badge_detail(request, track_name, badge_id):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  r.badge = get_object_or_404(Badge, pk=badge_id)
  r.user_track = get_user_track(request, track_name)
  if r.track != r.badge.requirement.level.track:
    raise Http404

  if request.user.is_authenticated():
    try:
      r.verification = Verification.objects.get(user=request.user, badge=r.badge)
      r.is_started = True
      r.is_unsubmitted = r.verification.status == Verification.UNSUBMITTED
      r.is_unverified = r.verification.status == Verification.UNVERIFIED
      r.is_verified = r.verification.status == Verification.VERIFIED
    except ObjectDoesNotExist:
      r.is_started = False

  return r.__dict__


@render_to('user_add.html')
def user_add(request):
  r = Response()
  return r.__dict__


@render_to('user_home.html')
def user_home(request, username):
  r = Response()
  r.target_user = get_object_or_404(User, username__iexact=username)
  return r.__dict__


@render_to('user_merits.html')
def user_merits(request, username, track_name):
  r = Response()
  r.user = get_object_or_404(User, username__iexact=username)
  if track_name:
    r.track = get_object_or_404(Track, pk__iexact=track_name)
  r.user_tracks = r.user.user_tracks.order_by('-level__rank', '-xp')
  return r.__dict__


@render_to('user_verify.html')
def user_verify(request, username):
  r = Response()
  r.target_user = get_object_or_404(User, username__iexact=username)
  return r.__dict__


@ajax_request
def ajax_get_wall_posts(request):
  r = Response()
  if request.method != 'GET':
    return Response.errors('Request must use GET; used: %s.' % request.method)

  errors = get_errors(request.GET, {
      'target_user': (RequiredValidator(), ModelValidator(User, int)),
      'paginate': (RequiredValidator(), BooleanValidator()),
      'since_pk': (ModelValidator(WallPost, int)),
      'verification_pk': (ModelValidator(Verification, int)),
  })
  if errors:
    return Response.errors(errors)

  target_user_pk = int(request.GET['target_user'])

  # Get all wall posts visible to the specified user.
  wall_posts = WallPost.objects.filter(
      Q(is_public=True) | Q(user=request.user) | Q(poster=request.user),
      user__pk=target_user_pk)

  if 'since_pk' in request.GET:
    wall_posts = wall_posts.filter(pk__lt=int(request.GET['since_pk']))

  if 'verification_pk' in request.GET:
    wall_posts = wall_posts.filter(verification__pk=int(request.GET['verification_pk']))

  # Always sort by newest first, allowing the client to reorder the posts, if necessary.
  wall_posts = wall_posts.order_by('-timestamp').all()

  if request.GET['paginate'] == 'true':
    # Ignore the last post, which is just used to decide whether has_next.
    wall_post_count = min(len(wall_posts), WALL_POSTS_PER_PAGE)
    wall_posts = wall_posts[:WALL_POSTS_PER_PAGE + 1]
  else:
    wall_post_count = len(wall_posts)

  r.wall_posts = []
  for i in xrange(wall_post_count):
    r.wall_posts.append(wall_posts[i].to_dict())
  r.has_next = len(wall_posts) > WALL_POSTS_PER_PAGE

  return r.__dict__


@ajax_request
def ajax_post_to_wall(request):
  r = Response()
  if request.method != 'POST':
    return Response.errors('Request must use POST; used: %s.' % request.method)

  # Posting User must be logged in.
  if not request.user.is_authenticated():
    return Response.errors('User is not logged in.')

  # Perform all the general validation.
  errors = get_errors(request.POST, {
      'text': (NonEmptyValidator(), StrippedLengthValidator(WallPost.MAX_TEXT_LENGTH)),
      'to': (RequiredValidator(), ModelValidator(User, int)),
      'is_public': (RequiredValidator(), BooleanValidator()),
      'verification_pk': (ModelValidator(Verification, int)),
  })
  if errors:
    return Response.errors(errors)

  # Extract the relevant data.
  text = request.POST['text'].strip()
  to_pk = int(request.POST['to'])
  is_public = request.POST['is_public'] == 'true'
  verification_pk = (int(request.POST['verification_pk'])
                     if 'verification_pk' in request.POST
                     else None)

  # Create and save the new WallPost.
  post = WallPost(poster=request.user, text=text, is_public=is_public)
  post.user_id = to_pk
  if verification_pk:
    post.verification_id = verification_pk
  post.save()
  r.post = post.to_dict()
  return r.__dict__


@ajax_request
def ajax_start_badge(request):
  r = Response()
  if request.method != 'POST':
    return Response.errors('Request must use POST; used: %s.' % request.method)

  # Posting User must be logged in.
  if not request.user.is_authenticated():
    return Response.errors('User is not logged in.')

  # Perform all the general validation.
  errors = get_errors(request.POST, {
      'badge': (RequiredValidator(), ModelValidator(Badge, int)),
  })
  if errors:
    return Response.errors(errors)

  badge = Badge.objects.get(pk=int(request.POST['badge']))
  if Verification.objects.filter(user=request.user, badge=badge).exists():
    return Response.errors('Badge already started.')

  if not request.user.user_tracks.filter(track__pk=badge.requirement.level.track.pk).exists():
    return Response.errors('User has not joined %s.' % badge.requirement.level.track.name)

  # Record that the badge has been started.
  verification = Verification(user=request.user, status=Verification.UNSUBMITTED)
  verification.badge = badge
  verification.save()

  return r.__dict__


@ajax_request
def ajax_complete_unverified_badge(request):
  r = Response()
  if request.method != 'POST':
    return Response.errors('Request must use POST; used: %s.' % request.method)

  # Posting User must be logged in.
  if not request.user.is_authenticated():
    return Response.errors('User is not logged in.')

  # Perform all the general validation.
  errors = get_errors(request.POST, {
      'badge': (RequiredValidator(), ModelValidator(Badge, int)),
  })
  if errors:
    return Response.errors(errors)

  badge = Badge.objects.get(pk=int(request.POST['badge']))
  if badge.requires_verification:
    return Response.errors('Badge requires verification.')

  try:
    user_track = request.user.user_tracks.get(track__pk=badge.requirement.level.track.pk)
  except ObjectDoesNotExist:
    return Response.errors('User has not joined %s.' % badge.requirement.level.track.name)

  try:
    verification = Verification.objects.get(user=request.user, badge=badge)
  except ObjectDoesNotExist:
    return Response.errors('Badge not started.')

  if verification.status != Verification.UNSUBMITTED:
    return Response.errors('Badge already completed.')

  # Award the badge and xp.
  user_track.badges.add(badge)
  user_track.xp += badge.xp()
  user_track.save()

  # Record that the badge has been completed.
  verification.status = Verification.VERIFIED
  verification.save()

  return r.__dict__


@ajax_request
def ajax_submit_verification(request):
  r = Response()
  if request.method != 'POST':
    return Response.errors('Request must use POST; used: %s.' % request.method)

  # Posting User must be logged in.
  if not request.user.is_authenticated():
    return Response.errors('User is not logged in.')

  # Perform all the general validation.
  errors = get_errors(request.POST, {
      'badge': (RequiredValidator(), ModelValidator(Badge, int)),
      'text_proof': (RequiredValidator()),
      'video_proof': (RequiredValidator(), YouTubeIdValidator()),
  })
  if errors:
    return Response.errors(errors)

  badge = Badge.objects.get(pk=int(request.POST['badge']))
  if not badge.requires_verification:
    return Response.errors('Badge does not require verification.')

  text_proof = request.POST['text_proof'].strip()
  video_proof = request.POST['video_proof']

  try:
    verification = Verification.objects.get(user=request.user, badge=badge)
  except ObjectDoesNotExist:
    return Response.errors('Badge not started.')

  if verification.status == Verification.VERIFIED:
    return Response.errors('Badge already completed.')

  # Update the data and open the request for verification.
  verification.text = text_proof
  verification.youtube_id = video_proof
  verification.status = Verification.UNVERIFIED
  verification.save()

  return r.__dict__


@ajax_request
def ajax_join_track(request):
  r = Response()
  if request.method != 'POST':
    return Response.errors('Request must use POST; used: %s.' % request.method)

  # Posting User must be logged in.
  if not request.user.is_authenticated():
    return Response.errors('User is not logged in.')

  # Perform all the general validation.
  errors = get_errors(request.POST, {
      'track': (RequiredValidator(), ModelValidator(Track, str)),
  })
  if errors:
    return Response.errors(errors)

  track_name = request.POST['track']
  if UserTrack.objects.filter(user=request.user, track__name=track_name).exists():
    return Response.errors('Track already joined.')

  # Create a new UserTrack.
  user_track = UserTrack(user=request.user, mission='')
  user_track.track_id = track_name
  try:
    user_track.level = Level.objects.get(track__name=track_name, rank=0)
  except ObjectDoesNotExist:
    return Response.errors('Track has no level 0.')
  user_track.save()

  return r.__dict__
