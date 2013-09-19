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
  if (post.verification) {
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
    target_user_pk: targetUserPk,
    paginate: paginate
  };
  if (paginate) {
    data.since_pk = earliestWallPostPks[targetUserPk];
  }
  if (opt_verificationPk) {
    data.verification_pk = opt_verificationPk;
  }
  $.ajax({
    url: '/x/get-wall-posts/',
    data: data,
    cache: false
  }).done(function (data) {
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
  }).fail(function() {
    $(wallSelector + ' .wall-load-error').text('Server error!');
  }).always(function () {
    enable($(wallSelector + ' .wall-load-button'));
  });
}

function postToWall(targetUserPk, isPublic, opt_verificationPk, opt_verify) {
  var wallSelector = buildWallSelector(targetUserPk);
  var text = trim($(wallSelector + ' .wall-post-textbox').val());

  if (text.length == 0) {
    if (opt_verify) {
      verify(opt_verificationPk, opt_verify);
      return;
    } else if (opt_verificationPk && opt_verify === false) {
      $(wallSelector + ' .wall-post-error').text(
          'You must provide an explanation to say "Needs more work."');
      return;  
    } else {
      return;
    }
  }

  disable($(wallSelector + ' .wall-post-box :input'));
  $(wallSelector + ' .wall-post-error').text('');

  var data = {
    text: text,
    to_pk: targetUserPk,
    is_public: isPublic
  };
  if (opt_verificationPk) {
    data.verification_pk = opt_verificationPk;
  }
  $.post('/x/post-to-wall/', data, function (data) {
    if (data.errors) {
      $(wallSelector + ' .wall-post-error').text(data.errors.join());
      return;
    }

    renderPost(targetUserPk, data.post).prependTo($(wallSelector + ' .wall'));
    $(wallSelector + ' .wall-post-textbox').val('');

    if (typeof opt_verify == 'boolean') {
      verify(opt_verificationPk, opt_verify);
    }
  }).fail(function () {
    $(wallSelector + ' .wall-post-error').text('Server error!');
  }).always(function () {
    enable($(wallSelector + ' .wall-post-box :input'));
  });
}