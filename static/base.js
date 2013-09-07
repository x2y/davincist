var activeBannerIndex = 0;
var bannerMessages = [];
var isShowingBanner = false;

function showBannerMessage(message) {
  bannerMessages.push(message);
  if (!isShowingBanner) {
    rotateBanner();
  }
}

function rotateBanner() {
  var $banners = $('.banner');
  $banners.eq(activeBannerIndex).fadeOut();
  activeBannerIndex = 1 - activeBannerIndex;

  isShowingBanner = bannerMessages.length > 0;
  if (isShowingBanner) {
    var message = bannerMessages[0];
    bannerMessages = bannerMessages.slice(1);

    var $activeBanner = $banners.eq(activeBannerIndex);
    var $activeBannerText = $activeBanner.find('.banner-text');
    $activeBannerText.text(message);
    $activeBanner.fadeIn();
    $activeBannerText.textFit({
      alignVert: true,
      alignHoriz: true,
      multiLine: true,
      reProcess: true,
      maxFontSize: 120
    });
    setTimeout(rotateBanner, 2500);
  }
}

function trim(s) {
  return s.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
}

function enable($elements) {
  if (!$.isArray($elements)) {
    $elements = [$elements];
  }
  for (var i = 0; i < $elements.length; ++i) {
    $elements[i].prop('disabled', false);
  }
}

function disable($elements) {
  if (!$.isArray($elements)) {
    $elements = [$elements];
  }
  for (var i = 0; i < $elements.length; ++i) {
    $elements[i].prop('disabled', true);
  }
}

function renderTemplate($template, data) {
  var $instance = $template.clone().removeClass('template');
  for (var key in data) {
    $instance.find('.' + key).text(data[key]);
  }
  return $instance;
}
