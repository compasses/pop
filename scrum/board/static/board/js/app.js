var app = (function($) {
  var config = $('#config'),
    app = JSON.parse(config.text());
  $(document).ready(function() {
    var router = new app.router();
  });
  console.log("start return app!");
  return app;
})(jQuery);
