from app.views import *
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


admin.autodiscover()

TRACK_REGEX = r'[^\s/]{1,64}'
TRACK_GROUP = r'(?P<track_name>%s)' % TRACK_REGEX

# LEVEL_REGEX = r'\d\d?'
# LEVEL_GROUP = r'(?P<level_id>%s)' % LEVEL_REGEX

QUEST_REGEX = r'\d{1,10}'
QUEST_GROUP = r'(?P<quest_id>%s)' % QUEST_REGEX

# BADGE_REGEX = r'\d{1,10}'
# BADGE_GROUP = r'(?P<badge_id>%s)' % BADGE_REGEX

USER_REGEX = r'[^\s/]{1,30}'
USER_GROUP = r'(?P<username>%s)' % USER_REGEX

urlpatterns = patterns('',
    # url(r'^(?i)admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),

    url(r'^(?i)$', home, name='home'),
    url(r'^(?i)about/$', about, name='about'),

    # Field pages.
    # url(r'^(?i)f/add$' % FIELD_GROUP, field_add, name='field_add'),
    # url(r'^(?i)f/all$', field_list, name='field_list'),
    # url(r'^(?i)f/%s$' % FIELD_GROUP, field_detail, name='field_detail'),
    # url(r'^(?i)f/%s/tracks$' % FIELD_GROUP, field_tracks, name='field_tracks'),
    # url(r'^(?i)f/%s/Users$' % FIELD_GROUP, field_users, name='field_users'),

    # Track pages.
    # url(r'^(?i)t/add$' % TRACK_GROUP, track_add, name='track_add'),
    url(r'^(?i)t/all$', track_list, name='track_list'),
    url(r'^(?i)t/%s/$' % TRACK_GROUP, track_detail, name='track_detail'),
    url(r'^(?i)t/%s/users/$' % TRACK_GROUP, track_users, name='track_users'),
    url(r'^(?i)t/%s/join/$' % TRACK_GROUP, track_join, name='track_join'),
    # url(r'^(?i)t/%s/leave$' % TRACK_GROUP, track_leave, name='track_leave'),
    # url(r'^(?i)t/%s/gallery$' % TRACK_GROUP, track_gallery, name='track_gallery'),

    url(r'^(?i)t/%s/levels/$' % TRACK_GROUP, track_levels, name='track_levels'),
    # url(r'^(?i)t/%s/level/add$' % TRACK_GROUP, level_add, name='level_add'),
    # url(r'^(?i)t/%s/level/%s$' % (TRACK_GROUP, LEVEL_GROUP), level_detail, name='level_detail'),
    # url(r'^(?i)t/%s/level/%s/edit$' % (TRACK_GROUP, LEVEL_GROUP), level_edit, name='level_edit'),
    # url(r'^(?i)t/%s/level/%s/delete$' % (TRACK_GROUP, LEVEL_GROUP), level_delete, name='level_delete'),

    url(r'^(?i)t/%s/quests/$' % TRACK_GROUP, track_quests, name='track_quests'),
    url(r'^(?i)t/%s/quests/verify/$' % TRACK_GROUP, quests_verify, name='quests_verify'),
    # url(r'^(?i)t/%s/quest/add$' % TRACK_GROUP, quest_add, name='quest_add'),
    url(r'^(?i)t/%s/quest/%s/$' % (TRACK_GROUP, QUEST_GROUP), quest_detail, name='quest_detail'),
    # url(r'^(?i)t/%s/quest/%s/edit$' % (TRACK_GROUP, QUEST_GROUP), quest_edit, name='quest_edit'),
    # url(r'^(?i)t/%s/quest/%s/delete$' % (TRACK_GROUP, QUEST_GROUP), quest_delete, name='quest_delete'),

    url(r'^(?i)t/%s/badges/$' % TRACK_GROUP, track_badges, name='track_badges'),
    # url(r'^(?i)t/%s/badge/%s$' % (TRACK_GROUP, BADGE_GROUP), badge_detail, name='badge_detail'),

    # User pages.
    url(r'^(?i)u/signup/$', user_add, name='user_add'),
    # url(r'^(?i)u/all$', user_list, name='user_list'),
    url(r'^(?i)u/%s/$' % USER_GROUP, user_home, name='user_home'),
    url(r'^(?i)u/%s/merits/' % USER_GROUP, user_merits, name='user_merits'),
    url(r'^(?i)u/%s/gallery/$' % USER_GROUP, user_gallery, name='user_gallery'),
    url(r'^(?i)u/%s/edit/' % USER_GROUP, user_edit, name='user_edit'),
    # url(r'^(?i)u/%s/delete' % USER_GROUP, user_delete, name='user_delete'),

    # AJAX pages.
    url(r'^(?i)x/get-wall-posts/', ajax_get_wall_posts, name='ajax_get_wall_posts'),
    url(r'^(?i)x/post-to-wall/', ajax_post_to_wall, name='ajax_post_to_wall'),
    url(r'^(?i)x/start-quest/', ajax_start_quest, name='ajax_start_quest'),
    url(r'^(?i)x/join-track/', ajax_join_track, name='ajax_join_track'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
