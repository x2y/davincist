var earliestWallPostPks = [];

function buildWallSelector(targetUserPk) {
  return '.wall-container.user-' + targetUserPk;
}

function renderPost(targetUserPk, post) {
  var templateParams = {
    poster: post.poster,
    text: post.text,
    timestamp: new Date(post.timestamp * 1000).toLocaleString()
  };
  if (post.verification != null) {
    templateParams.verification = ' re: ' + post.verification.badge;
  }
  var wallSelector = buildWallSelector(targetUserPk);
  var postClass = wallSelector + ' ' + (post.is_public ? '.public-post' : '.private-post');
  return renderTemplate($(postClass + '.template'), templateParams);
}

function loadWallPosts(targetUserPk, paginate, opt_verificationPk) {
  var wallSelector = buildWallSelector(targetUserPk);
  $(wallSelector + ' .wall-load-error').text(''); 

  var data = {
    target_user: targetUserPk,
    paginate: paginate
  };
  if (paginate) {
    data.since_pk = earliestWallPostPks[targetUserPk];
  }
  if (opt_verificationPk != null) {
    data.verification_pk = opt_verificationPk;
  }
  $.ajax({
    url: '/x/get-wall-posts/',
    data: data,
    cache: false,
    success: function (data) {
      if (data.errors) {
        $(wallSelector + ' .wall-load-error').text(data.errors.join());
        return;
      }
      var $wall = $(wallSelector + ' .wall');
      for (var i = 0; i < data.wall_posts.length; ++i) {
        var post = data.wall_posts[i];
        renderPost(targetUserPk, post).appendTo($wall);
        if (paginate) {
          earliestWallPostPks[targetUserPk] = post.pk;
          if (!data.has_next) {
            $(wallSelector + ' .wall-load-button').remove();
          }
        }
      }
    }
  }).fail(function() {
    $(wallSelector + ' .wall-load-error').text('Server error!');
  }).always(function () {
    enable($(wallSelector + ' .wall-load-button'));
  });
}

function postToWall(targetUserPk, isPublic, opt_verificationPk) {
  var wallSelector = buildWallSelector(targetUserPk);
  disable($(wallSelector + ' .wall-post-box :input'));
  $(wallSelector + ' .wall-post-error').text('');

  var data = {
    text: $(wallSelector + ' .wall-post-textbox').val(),
    to: targetUserPk,
    is_public: isPublic
  };
  if (opt_verificationPk != null) {
    data.verification_pk = opt_verificationPk;
  }
  $.post('/x/post-to-wall/', data, function (data) {
    if (data.errors) {
      $(wallSelector + ' .wall-post-error').text(data.errors.join());
      return;
    }

    renderPost(targetUserPk, data.post).prependTo($(wallSelector + ' .wall'));
    $(wallSelector + ' .wall-post-textbox').val('');
  }).fail(function () {
    $(wallSelector + ' .wall-post-error').text('Server error!');
  }).always(function () {
    enable($(wallSelector + ' .wall-post-box :input'));
  });
}