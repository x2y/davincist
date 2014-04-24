from models import *



def booleans(request):
  return {
      'True': True,
      'False': False,
  }


def navbar_data(request):
  user = request.user
  if not user.is_authenticated():
    return {}

  user_tracks = user.user_tracks
  return {
    'unjoined_tracks': Track.objects.exclude(pk__in=user_tracks.values_list('track__pk')),
    'user_tracks': user_tracks.order_by('-xp'),
  }
