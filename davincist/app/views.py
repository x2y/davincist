from annoying.decorators import render_to
from django.shortcuts import *
from models import *
from django.core.exceptions import ObjectDoesNotExist


# Attributes will be defined outside init pylint: disable=W0201
class Response(object):
  pass


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

  return r.__dict__


@render_to('track_quests.html')
def track_quests(request, track_name):
  r = Response()
  r.track = get_object_or_404(Track, pk__iexact=track_name)
  if not request.user.is_anonymous():
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
  r.user = get_object_or_404(User, username__iexact=username)
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

