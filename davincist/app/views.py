from annoying.decorators import render_to
from django.shortcuts import *
from models import *


# Attributes will be defined outside init pylint: disable=W0201
class Response(object):
  pass


@render_to('home.html')
def home(request):
  r = Response()
  return r.__dict__


@render_to('about.html')
def about(request):
  r = Response()
  return r.__dict__


@render_to('path_detail.html')
def path_detail(request, path_name):
  r = Response()
  r.path = get_object_or_404(Path, pk__iexact=path_name)
  return r.__dict__


@render_to('path_users.html')
def path_users(request, path_name):
  r = Response()
  r.path = get_object_or_404(Path, pk__iexact=path_name)
  return r.__dict__


@render_to('path_join.html')
def path_join(request, path_name):
  r = Response()
  r.path = get_object_or_404(Path, pk_iexact=path_name)
  return r.__dict__


@render_to('path_levels.html')
def path_levels(request, path_name):
  r = Response()
  r.path = get_object_or_404(Path, pk__iexact=path_name)

  return r.__dict__


@render_to('path_quests.html')
def path_quests(request, path_name):
  r = Response()
  r.path = get_object_or_404(Path, pk__iexact=path_name)
  return r.__dict__


@render_to('quest_submit.html')
def quest_submit(request, path_name, quest_id):
  r = Response()
  r.path = get_object_or_404(Path, pk__iexact=path_name)
  r.quest = get_object_or_404(Quest, pk=quest_id)
  return r.__dict__


@render_to('quests_verify.html')
def quests_verify(request, path_name):
  r = Response()
  r.path = get_object_or_404(Path, pk__iexact=path_name)
  return r.__dict__


@render_to('path_badges.html')
def path_badges(request, path_name):
  r = Response()
  r.path = get_object_or_404(Path, pk__iexact=path_name)
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

