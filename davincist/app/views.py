from annoying.decorators import ajax_request, render_to
from django.shortcuts import *
from models import *
from django.core.exceptions import ObjectDoesNotExist


# Attributes will be defined outside init pylint: disable=W0201
class Response(object):
  pass

  @classmethod
  def errors(cls, *errors):
    print errors
    if len(errors) == 1 and hasattr(errors[0], '__iter__'):
      return {'errors': errors[0]}
    else:
      return {'errors': errors}


def get_missing_field_errors(data, fields):
  ret = []
  for field in fields:
    if field not in data:
      ret.append('Missing field: %s.' % field)
    elif not data[field].strip():
      ret.append('Empty field: %s.' % field)
  return ret


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


@render_to('quest_submit.html')
def quest_submit(request, track_name, quest_id):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  r.quest = get_object_or_404(Quest, pk=quest_id)
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
def ajax_post_to_wall(request):
  r = Response()
  if request.method != 'POST':
    return Response.errors('Request must use POST; used: %s.' % request.method)

  # Posting User must be logged in.
  if not request.user.is_authenticated():
    return Response.errors('User is not logged in.')

  # Request must have text, to, and is_public fields filled in.
  data = request.POST
  errors = get_missing_field_errors(data, ('text', 'to', 'is_public'))
  if errors:
    return Response.errors(errors)

  text_field, to_field, is_public_field = data['text'], data['to'], data['is_public']

  # Request must have a valid text field.
  text = text_field.strip()
  if len(text) > WallPost.MAX_TEXT_LENGTH:
    return Response.errors('Invalid text field: >%d chars' % WallPost.MAX_TEXT_LENGTH)

  # Request must have a valid to field.
  if not to_field.isdigit():
    return Response.errors('Invalid to field: %s.' % to_field)
  try:
    to = User.objects.get(pk=int(to_field))
  except ObjectDoesNotExist:
    return Response.errors('No User with pk: %s.' % to_field)

  # Request must have a valid is_public field.
  if is_public_field not in ('true', 'false'):
    return Response.errors('Invalid is_public field: %s.' % to_field)
  is_public = is_public_field == 'true'

  # Create and save the new WallPost.
  post = WallPost(user=to, poster=request.user, text=text_field, is_public=is_public)
  post.save()
  r.post = post.to_dict()
  return r.__dict__
