parking.factory('parkingService', function(parkingConfig) {
  var _calculateTicket = function(car) {
    var departHour = new Date.getHours(),
        entranceHour = car.entrance.getHours(),
        parkingPeriod = departHour - entranceHour,
        parkingPrice = parkingPeriod * parkingConfig.parkingRate;
        return {
          period: parkingPeriod,
          price: parkingPrice
        };
  };
  return {
    calculateTicket: _calculateTicket
  };
});
