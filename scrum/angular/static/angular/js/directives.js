parking.directive("alert", function() {
  return {
    restrict: 'E',
    scope: {
      topic: '=',
      description: '=',
      close: '&'
    },
    templateUrl: "/alert.html",
    replace: true
  };
});

parking.directive("accordionItem", function() {
  return {
    templateUrl: "/accordionItem.html",
    restrict: "E",
    scope: {
      title: "@",
    },
    transclude: true,
    link: function(scope, element, attrs, ctrl, transcludeFn) {
      element.bind("click", function() {
        scope.$apply(function() {
          scope.active = !scope.active;
        });
      });
    }
  };
});
