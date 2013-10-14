from app.views import *
from app.social_auth_pipeline_views import *
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


admin.autodiscover()

TRACK_REGEX = r'[^\s/]{1,64}'
TRACK_GROUP = r'(?P<track_name>%s)' % TRACK_REGEX

BADGE_REGEX = r'\d{1,10}'
BADGE_GROUP = r'(?P<badge_id>%s)' % BADGE_REGEX

USER_REGEX = r'[^\s/]{1,30}'
USER_GROUP = r'(?P<username>%s)' % USER_REGEX

VERIFICATION_REGEX = r'\d{1,10}'
VERIRIFICATION_GROUP = r'(?P<verification_id>%s)' % VERIFICATION_REGEX

urlpatterns = patterns(
    '',
    # Third-party pages.
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),

    # Top-level pages.
    url(r'^(?i)$', home, name='home'),
    url(r'^(?i)about/$', about, name='about'),
    url(r'^(?i)request-invite/$', request_invite, name='request_invite'),

    # Track pages.
    url(r'^(?i)t/all$', track_list, name='track_list'),
    url(r'^(?i)t/%s/$' % TRACK_GROUP, track_detail, name='track_detail'),
    url(r'^(?i)t/%s/users/$' % TRACK_GROUP, track_users, name='track_users'),
    url(r'^(?i)t/%s/badge/%s/$' % (TRACK_GROUP, BADGE_GROUP), badge_detail, name='badge_detail'),

    # User pages.
    url(r'^(?i)u/signup/$', user_add, name='user_add'),
    url(r'^(?i)u/%s/$' % USER_GROUP, user_home, name='user_home'),
    url(r'^(?i)u/%s/merits/(?:%s/)?' % (USER_GROUP, TRACK_GROUP), user_merits, name='user_merits'),
    url(r'^(?i)u/%s/verify/$' % USER_GROUP, user_verify, name='user_verify'),

    # Partial pages.
    url(r'^(?i)p/verification/%s/$' % VERIRIFICATION_GROUP, verification, name='verification'),

    # AJAX pages.
    url(r'^(?i)x/get-wall-posts/', ajax_get_wall_posts, name='ajax_get_wall_posts'),
    url(r'^(?i)x/post-to-wall/', ajax_post_to_wall, name='ajax_post_to_wall'),
    url(r'^(?i)x/start-badge/', ajax_start_badge, name='ajax_start_badge'),
    url(r'^(?i)x/complete-unverified-badge/', ajax_complete_unverified_badge, name='ajax_complete_unverified_badge'),
    url(r'^(?i)x/submit-verification/', ajax_submit_verification, name='ajax_submit_verification'),
    url(r'^(?i)x/get-verifications/', ajax_get_verifications, name='ajax_get_verifications'),
    url(r'^(?i)x/submit-invite-request/', ajax_submit_invite_request, name='ajax_submit_invite_request'),
    url(r'^(?i)x/verify/', ajax_verify, name='ajax_verify'),
    url(r'^(?i)x/join-track/', ajax_join_track, name='ajax_join_track'),

    # Authentication flow pages.
    url(r'^login-error/$', login_error, name='login_error'),
    url(r'^form/$', form, name='form'),
    url(r'^form2/$', form2, name='form2'),
    url(r'^close_login_popup/$', close_login_popup, name='login_popup_close'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
