from annoying.decorators import ajax_request, render_to
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
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


@render_to('home.html')
def home(request):
  r = Response()
  r.tracks = Track.objects.all()
  return r.__dict__


@render_to('about.html')
def about(request):
  r = Response()
  return r.__dict__


@render_to('track_detail.html')
def track_detail(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  return r.__dict__


@render_to('track_list.html')
def track_list(request):
  r = Response()
  r.tracks = Track.objects.all()
  return r.__dict__


@render_to('track_users.html')
def track_users(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  return r.__dict__


@render_to('track_join.html')
def track_join(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  return r.__dict__


@render_to('track_levels.html')
def track_levels(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  if request.user.is_authenticated():
    try:
      r.user_track = request.user.user_tracks.get(track__name=track_name)
    except ObjectDoesNotExist:
      pass
  return r.__dict__


@render_to('track_quests.html')
def track_quests(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  if request.user.is_authenticated():
    try:
      r.user_track = request.user.user_tracks.get(track__name=track_name)
    except ObjectDoesNotExist:
      pass
  return r.__dict__


@render_to('quest_detail.html')
def quest_detail(request, track_name, quest_id):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  r.quest = get_object_or_404(Quest, pk=quest_id)
  if r.track != r.quest.level.track:
    raise Http404

  try:
    r.quest_status = VerificationRequest.objects.get(user=request.user, quest=r.quest).status
  except ObjectDoesNotExist:
    pass

  return r.__dict__


@render_to('quests_verify.html')
def quests_verify(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  return r.__dict__


@render_to('track_badges.html')
def track_badges(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
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


@render_to('use_merits.html')
def user_merits(request, username):
  r = Response()
  r.user = get_object_or_404(User, username__iexact=username)
  return r.__dict__


@render_to('user_gallery.html')
def user_gallery(request, username):
  r = Response()
  r.user = get_object_or_404(User, username__iexact=username)
  return r.__dict__


@render_to('user_edit.html')
def user_edit(request, username):
  r = Response()
  r.user = get_object_or_404(User, username__iexact=username)
  return r.__dict__


@ajax_request
def ajax_get_wall_posts(request):
  r = Response()
  if request.method != 'GET':
    return Response.errors('Request must use GET; used: %s.' % request.method)

  errors = get_errors(request.GET, {
      'target_user': (RequiredValidator(), ModelValidator(User)),
      'page': (RequiredValidator(), IntegerValidator()),
  })
  if errors:
    return Response.errors(errors)

  target_user = User.objects.get(pk=int(request.GET['target_user']))
  page_number = int(request.GET['page'])

  # Get all wall posts visible to the specified user (paginated).
  wall_posts = target_user.wall_posts.filter(Q(is_public=True) |
                                             Q(user=request.user) |
                                             Q(poster=request.user)).order_by('-timestamp')
  paginator = Paginator(wall_posts, WALL_POSTS_PER_PAGE)

  r.wall_posts = []
  try:
    page = paginator.page(page_number)
    for wall_post in page:
      r.wall_posts.append(wall_post.to_dict())
    r.has_next = page.has_next()
  except EmptyPage:
    r.has_next = False
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
      'to': (RequiredValidator(), ModelValidator(User)),
      'is_public': (RequiredValidator(), BooleanValidator()),
  })
  if errors:
    return Response.errors(errors)

  # Extract the relevant data.
  text = request.POST['text'].strip()
  to = User.objects.get(pk=int(request.POST['to']))
  is_public = request.POST['is_public'] == 'true'

  # TODO: Support quest verification linking.

  # Create and save the new WallPost.
  post = WallPost(user=to, poster=request.user, text=text, is_public=is_public)
  post.save()
  r.post = post.to_dict()
  return r.__dict__


@ajax_request
def ajax_start_quest(request):
  r = Response()
  if request.method != 'POST':
    return Response.errors('Request must use POST; used: %s.' % request.method)

  # Posting User must be logged in.
  if not request.user.is_authenticated():
    return Response.errors('User is not logged in.')

  # Perform all the general validation.
  errors = get_errors(request.POST, {
      'quest': (RequiredValidator(), ModelValidator(Quest)),
  })
  if errors:
    return Response.errors(errors)

  quest_pk = int(request.POST['quest'])
  if VerificationRequest.objects.filter(user=request.user, quest__pk=quest_pk).exists():
    return Response.errors('Quest already started!')

  # Record that the quest has been started.
  verification_request = VerificationRequest(user=request.user,
                                             status=VerificationRequest.UNSUBMITTED)
  verification_request.quest_id = quest_pk
  verification_request.save()

  return r.__dict__
