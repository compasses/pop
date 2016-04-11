parking.controller("parkingCtrl", function($scope, $filter) {
  $scope.appTitle = $filter("uppercase")("[Packt] Parking");
  $scope.cars = [];
  $scope.colors = ["White", "Black", "Blue", "Red", "Silver"];
  $scope.park = function(car) {
    car.entrance = new Date();
    $scope.cars.push(car);
    delete $scope.car;
  };
  $scope.showAlert = true;
  $scope.alertTopic = "Something went wrong!";
  $scope.alertMessage = "You must inform the plate and the color of the car!";
  $scope.closeAlert = function() {
    $scope.showAlert = false;
  };
});
