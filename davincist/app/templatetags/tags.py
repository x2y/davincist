from django import template


register = template.Library()


@register.inclusion_tag('badge_link_tag.html')
def badge_link(badge, link_to_verification=False, target_username=None):
  return {
      'badge': badge,
      'link_to_verification': link_to_verification,
      'target_username': target_username,
  }


@register.inclusion_tag('level_link_tag.html')
def level_link(level):
  return {'level': level}


@register.inclusion_tag('track_link_tag.html')
def track_link(track):
  return {'track': track}


@register.inclusion_tag('user_link_tag.html')
def user_link(user):
  return {'user': user}
