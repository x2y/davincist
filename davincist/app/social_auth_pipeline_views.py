from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version
from social_auth.utils import setting


def form(request):
  if request.method == 'POST' and request.POST.get('username'):
    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    request.session['saved_username'] = request.POST['username']
    backend = request.session[name]['backend']
    return redirect('socialauth_complete', backend=backend)
  return render_to_response('form.html', {}, RequestContext(request))


def form2(request):
  if request.method == 'POST' and request.POST.get('first_name'):
    request.session['saved_first_name'] = request.POST['first_name']
    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    backend = request.session[name]['backend']
    return redirect('socialauth_complete', backend=backend)
  return render_to_response('form2.html', {}, RequestContext(request))


def redirect_to_form(*args, **kwargs):
  if not kwargs['request'].session.get('saved_username') and kwargs.get('user') is None:
    return HttpResponseRedirect('/form/')


def username(request, *args, **kwargs):
  if kwargs.get('user'):
    username = kwargs['user'].username
  else:
    username = request.session.get('saved_username')
  return {'username': username}


def redirect_to_form2(*args, **kwargs):
  if not kwargs['request'].session.get('saved_first_name'):
    return HttpResponseRedirect('/form2/')


def first_name(request, *args, **kwargs):
  if 'saved_first_name' in request.session:
    user = kwargs['user']
    user.first_name = request.session.get('saved_first_name')
    user.save()


def close_login_popup(request):
    return render_to_response('close_popup.html', {}, RequestContext(request))
