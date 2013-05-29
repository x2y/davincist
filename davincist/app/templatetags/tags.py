from davincist.app import models
from django import template
import os.path

register = template.Library()

@register.inclusion_tag('badge_link_tag.html')
def badge_link(badge):
  return {'badge': badge}

@register.inclusion_tag('level_link_tag.html')
def level_link(level):
  return {'level': level}

@register.inclusion_tag('path_link_tag.html')
def path_link(path):
  return {'path': path}
  
@register.inclusion_tag('crest_link_tag.html')
def crest_link(crest):
#  if os.path.isfile(str(crest)):
#    return {'crest': crest}
#  else:
#    return {'crest': 'nocrest'}
  return {'crest': crest}

@register.inclusion_tag('quest_link_tag.html')
def quest_link(quest):
  return {'quest': quest}

@register.inclusion_tag('user_link_tag.html')
def user_link(user):
  return {'user': user}
