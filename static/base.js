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
