(function($) {
  $.ajaxSetup({
    'beforeSend': function(xhr) {
      xhr.setRequestHeader("accept", "application/json");
    }
  });
})(jQuery);