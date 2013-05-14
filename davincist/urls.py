from app.views import *
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

PATH_REGEX = r'[^\s/]{1,64}'
PATH_GROUP = r'(?P<path_name>%s)' % PATH_REGEX

# LEVEL_REGEX = r'\d\d?'
# LEVEL_GROUP = r'(?P<level_id>%s)' % LEVEL_REGEX

QUEST_REGEX = r'\d{1,10}'
QUEST_GROUP = r'(?P<quest_id>%s)' % QUEST_REGEX

# BADGE_REGEX = r'\d{1,10}'
# BADGE_GROUP = r'(?P<badge_id>%s)' % BADGE_REGEX

USER_REGEX = r'[^\s/]{1,32}'
USER_GROUP = r'(?P<user_id>%s)' % USER_REGEX

urlpatterns = patterns('',
    # url(r'(?i)^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'(?i)^$', home, name='home'),
    url(r'(?i)^about/$', about, name='about'),

    # Field pages.
    # url(r'(?i)^f/add$' % FIELD_GROUP, field_add, name='field_add'),
    # url(r'(?i)^f/all$', field_list, name='field_list'),
    # url(r'(?i)^f/%s$' % FIELD_GROUP, field_detail, name='field_detail'),
    # url(r'(?i)^f/%s/paths$' % FIELD_GROUP, field_paths, name='field_paths'),
    # url(r'(?i)^f/%s/Users$' % FIELD_GROUP, field_users, name='field_users'),

    # Path pages.
    # url(r'(?i)^p/add$' % PATH_GROUP, path_add, name='path_add'),
    # url(r'(?i)^p/all$', path_list, name='path_list'),
    url(r'(?i)^p/%s/$' % PATH_GROUP, path_detail),
    url(r'(?i)^p/%s/users/$' % PATH_GROUP, path_users, name='path_users'),
    url(r'(?i)^p/%s/join/$' % PATH_GROUP, path_join, name='path_join'),
    # url(r'(?i)^p/%s/leave$' % PATH_GROUP, path_leave, name='path_leave'),
    # url(r'(?i)^p/%s/gallery$' % PATH_GROUP, path_gallery, name='path_gallery'),

    url(r'(?i)^p/%s/levels/$' % PATH_GROUP, path_levels, name='path_levels'),
    # url(r'(?i)^p/%s/level/add$' % PATH_GROUP, level_add, name='level_add'),
    # url(r'(?i)^p/%s/level/%s$' % (PATH_GROUP, LEVEL_GROUP), level_detail, name='level_detail'),
    # url(r'(?i)^p/%s/level/%s/edit$' % (PATH_GROUP, LEVEL_GROUP), level_edit, name='level_edit'),
    # url(r'(?i)^p/%s/level/%s/delete$' % (PATH_GROUP, LEVEL_GROUP), level_delete, name='level_delete'),

    url(r'(?i)^p/%s/quests/$' % PATH_GROUP, path_quests, name='path_quests'),
    url(r'(?i)^p/%s/quests/verify/$' % PATH_GROUP, quests_verify, name='quests_verify'),
    # url(r'(?i)^p/%s/quest/add$' % PATH_GROUP, quest_add, name='quest_add'),
    url(r'(?i)^p/%s/quest/%s/submit/$' % (PATH_GROUP, QUEST_GROUP), quest_submit, name='quest_submit'),
    # url(r'(?i)^p/%s/quest/%s/edit$' % (PATH_GROUP, QUEST_GROUP), quest_edit, name='quest_edit'),
    # url(r'(?i)^p/%s/quest/%s/delete$' % (PATH_GROUP, QUEST_GROUP), quest_delete, name='quest_delete'),

    url(r'(?i)^p/%s/badges/$' % PATH_GROUP, path_badges, name='path_badges'),
    # url(r'(?i)^p/%s/badge/%s$' % (PATH_GROUP, BADGE_GROUP), badge_detail, name='badge_detail'),

    # User pages.
    url(r'(?i)^u/signup/$', user_add, name='user_add'),
    # url(r'(?i)^u/all$', user_list, name='user_list'),
    url(r'(?i)^u/%s/$' % USER_GROUP, user_home, name='user_home'),
    url(r'(?i)^u/%s/merits/' % USER_GROUP, user_merits, name='user_merits'),
    url(r'(?i)^u/%s/gallery/$' % USER_GROUP, user_gallery, name='user_gallery'),
    url(r'(?i)^u/%s/edit/' % USER_GROUP, user_edit, name='user_edit'),
    # url(r'(?i)^u/%s/delete' % USER_GROUP, user_delete, name='user_delete'),
)

