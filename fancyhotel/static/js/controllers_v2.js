var resourceModule = angular.module('resourceModule', ['ngResource']);

function apiErrorMessage(error, fallback) {
  fallback = fallback || 'No se pudo completar la operación.';
  if (!error) {
    return fallback;
  }
  if (error.status === 0) {
    return 'No hay conexión con el servidor. Verifica que la app esté en ejecución.';
  }
  var data = error.data;
  if (!data) {
    return fallback;
  }
  if (typeof data === 'string') {
    return data;
  }
  if (data.error) {
    return data.error;
  }
  if (data.message) {
    if (typeof data.message === 'string') {
      return data.message;
    }
    var keys = Object.keys(data.message);
    if (keys.length) {
      return data.message[keys[0]];
    }
  }
  return fallback;
}

resourceModule.factory('authFactory', function($resource) {
  return $resource('/api', {}, {
    Register: {
      method: 'POST',
      url: '/api/register',
      headers: { 'Content-Type': 'application/json;charset=utf-8' }
    },
    Login: { method: 'POST', url: '/api/login' },
    Logout: { method: 'POST', url: '/api/logout' }
  });
});

resourceModule.factory('reportFactory', function($resource) {
  return $resource('/api', {}, {
    ResReport: { method: 'GET', url: '/api/reports/reservation' },
    PopularRoomCatReport: { method: 'GET', url: '/api/reports/popularRoom' },
    RevenueReport: { method: 'GET', url: '/api/reports/revenue' },
    DemandForecast: { method: 'GET', url: '/api/reports/demandForecast' },
    Confirmations: { method: 'GET', url: '/api/confirmations', isArray: true }
  });
});

resourceModule.factory('pricingFactory', function($resource) {
  return $resource('/api', {}, {
    List: { method: 'GET', url: '/api/price-rules', isArray: true },
    Create: { method: 'POST', url: '/api/price-rules' }
  });
});

resourceModule.factory('reservationFactory', function($resource) {
  return $resource('/api', {}, {
    SearchRooms: { method: 'GET', url: '/api/searchRoom' },
    Calendar: { method: 'GET', url: '/api/availability/calendar' },
    GetReservation: { method: 'GET', url: '/api/reservation/:reservation_id' },
    MakeReservation: { method: 'POST', url: '/api/reservation/create' },
    UpdateReservationConfirm: { method: 'GET', url: '/api/reservation/:reservation_id/availability' },
    UpdateReservation: { method: 'PUT', url: '/api/reservation/:reservation_id' },
    CancelReservation: { method: 'GET', url: '/api/reservation/:reservation_id/cancel' }
  });
});

resourceModule.factory('reviewFactory', function($resource) {
  return $resource('/api', {}, {
    AddReview: { method: 'POST', url: '/api/review' },
    GetReviews: { method: 'GET', url: '/api/review', isArray: true }
  });
});

resourceModule.factory('paymentFactory', function($resource) {
  return $resource('/api', {}, {
    GetCreditCards: { method: 'GET', url: '/api/payment', isArray: true },
    AddCreditCard: { method: 'POST', url: '/api/payment' },
    DeleteCreditCard: { method: 'DELETE', url: '/api/payment' },
    GetReservationByCardNumber: { method: 'GET', url: '/api/reservation/cardNumber', isArray: true }
  });
});

angular.module('FancyHotelApp', ['ngRoute', 'ngResource', 'resourceModule'])

.controller('shellController', function($rootScope, $scope, $location, authFactory, $window) {
  function syncSession() {
    $scope.currentUser = $rootScope.currentUser;
    $scope.userType = $rootScope.userType;
    $scope.loggedInBool = $rootScope.alreadyLoggedIn();
  }
  syncSession();
  $scope.path = $location.path();
  $scope.isLoggedIn = function() {
    return $rootScope.currentUser !== '';
  };
  $scope.logout = function() {
    authFactory.Logout({}, function() {
      $rootScope.clearSession();
      syncSession();
      $window.location.href = '#/login';
    });
  };
  $scope.$watch(function() { return $rootScope.currentUser; }, syncSession);
  $scope.$watch(function() { return $rootScope.userType; }, syncSession);
  $scope.$on('$routeChangeSuccess', function() {
    $scope.path = $location.path();
  });
})

.run(function($rootScope) {
  $rootScope.currentUser = localStorage.getItem('fancyhotel.user') || '';
  $rootScope.userType = localStorage.getItem('fancyhotel.role') || '';
  $rootScope.alreadyLoggedIn = function() {
    return $rootScope.currentUser !== '';
  };
  $rootScope.setSession = function(username, role) {
    $rootScope.currentUser = username;
    $rootScope.userType = role;
    localStorage.setItem('fancyhotel.user', username);
    localStorage.setItem('fancyhotel.role', role);
  };
  $rootScope.clearSession = function() {
    $rootScope.currentUser = '';
    $rootScope.userType = '';
    localStorage.removeItem('fancyhotel.user');
    localStorage.removeItem('fancyhotel.role');
  };
  $rootScope.locations = ['Atlanta', 'Charlotte', 'Savannah', 'Orlando', 'Miami'];
  $rootScope.roomTypes = ['Single', 'Double', 'Suite'];
})

.controller('registerController', function($scope, authFactory, $window) {
  $scope.username = 'C';
  $scope.myRegex = /^C[a-zA-Z0-9]{4}$/;
  $scope.submit = function() {
    var username = ($scope.username || '').trim().toUpperCase();
    if (!$scope.myRegex.test(username)) {
      window.alert('Usuario inválido: usa C seguido de 4 letras o números (ejemplo C1234).');
      return;
    }
    if (($scope.password || '').length < 6) {
      window.alert('La contraseña debe tener al menos 6 caracteres.');
      return;
    }
    if ($scope.confirmPass !== $scope.password) {
      window.alert('Las contraseñas no coinciden.');
      return;
    }
    authFactory.Register({
      username: username,
      email: ($scope.email || '').trim(),
      password: $scope.password,
      firstName: ($scope.firstName || '').trim(),
      lastName: ($scope.lastName || '').trim()
    }, function() {
      window.alert('Cuenta creada. Ahora puedes iniciar sesión.');
      $window.location.href = '#/login';
    }, function(error) {
      window.alert(apiErrorMessage(error, 'No se pudo registrar la cuenta.'));
    });
  };
})

.controller('loginController', function($rootScope, $scope, authFactory, $window) {
  $scope.submit = function() {
    authFactory.Login({ username: $scope.username, password: $scope.password }, function(data) {
      $rootScope.setSession(data.username, data.role);
      $window.location.href = '#/portal';
    }, function() {
      window.alert('Invalid credentials');
    });
  };
})

.controller('portalController', function($rootScope, $scope) {
  $scope.loggedInBool = $rootScope.alreadyLoggedIn();
})

.controller('reservationController', function($rootScope, $scope, $window, reservationFactory, paymentFactory) {
  function isoDate(date) {
    return date.toISOString().slice(0, 10);
  }
  var now = new Date();
  var tomorrow = new Date();
  tomorrow.setDate(now.getDate() + 1);

  $scope.loggedInBool = $rootScope.alreadyLoggedIn();
  $scope.location = 'Atlanta';
  $scope.roomType = '';
  $scope.maxPrice = '';
  $scope.checkIn = isoDate(now);
  $scope.checkOut = isoDate(tomorrow);
  $scope.calendarMonth = $scope.checkIn.slice(0, 7);
  $scope.roomsAvailable = [];
  $scope.selectedRooms = {};
  $scope.extra_beds = {};
  $scope.total_cost = 0;
  $scope.creditCards = [];
  $scope.hideForm = false;
  $scope.confirmationPage = false;
  $scope.viewPart1 = true;
  $scope.viewPart2 = false;
  $scope.viewPart3 = false;
  $scope.cancelView1 = true;
  $scope.cancelView2 = false;
  $scope.today = new Date();

  paymentFactory.GetCreditCards({ username: $rootScope.currentUser }, function(cards) {
    $scope.creditCards = cards;
    if (cards.length > 0) {
      $scope.cardLast4 = cards[0].last4;
    }
  });

  $scope.submit = function() {
    reservationFactory.SearchRooms({
      location: $scope.location,
      checkIn: $scope.checkIn,
      checkOut: $scope.checkOut,
      roomType: $scope.roomType || undefined,
      maxPrice: $scope.maxPrice || undefined
    }, function(data) {
      $scope.roomsAvailable = data.response;
      $scope.hideForm = true;
      $scope.error = data.result ? '' : 'No rooms match those dates and filters.';
    });
  };

  $scope.loadCalendar = function() {
    reservationFactory.Calendar({ location: $scope.location, month: $scope.calendarMonth }, function(data) {
      $scope.calendar = data;
    });
  };

  $scope.updateTotalCost = function() {
    var nights = Math.max(0, (new Date($scope.checkOut) - new Date($scope.checkIn)) / 86400000);
    $scope.total_cost = 0;
    angular.forEach($scope.roomsAvailable, function(room) {
      if ($scope.selectedRooms[room.location + room.room_number]) {
        $scope.total_cost += room.cost;
        if ($scope.extra_beds[room.location + room.room_number]) {
          $scope.total_cost += room.extra_bed_price;
        }
      }
    });
    $scope.total_cost *= nights;
  };

  $scope.bookRooms = function() {
    var rooms = [];
    angular.forEach($scope.roomsAvailable, function(room) {
      if ($scope.selectedRooms[room.location + room.room_number]) {
        rooms.push({
          room_number: room.room_number,
          location: room.location,
          cost: room.cost,
          extra_bed_price: room.extra_bed_price,
          extra_bed_or_not: $scope.extra_beds[room.location + room.room_number] ? '1' : '0'
        });
      }
    });
    if (rooms.length === 0) {
      window.alert('Select at least one room.');
      return;
    }
    reservationFactory.MakeReservation({
      username: $rootScope.currentUser,
      checkIn: $scope.checkIn,
      checkOut: $scope.checkOut,
      card_last4: $scope.cardLast4,
      rooms: rooms
    }, function(data) {
      $scope.confirmationData = data;
      $scope.confirmationPage = true;
    }, function(error) {
      window.alert(error.data.message || 'Reservation failed.');
    });
  };

  $scope.findReservation = function() {
    reservationFactory.GetReservation({ reservation_id: $scope.resID, username: $rootScope.currentUser }, function(data) {
      $scope.cancelView1 = false;
      $scope.cancelView2 = true;
      $scope.viewPart2 = true;
      $scope.viewPart1 = false;
      $scope.currRes = data.data;
      $scope.refund_amount = $scope.refundAmount($scope.currRes.checkin_date, $scope.currRes.total_cost);
      $scope.cancel_cost = $scope.currRes.total_cost - $scope.refund_amount;
    }, function() {
      window.alert('Reservation not found.');
    });
  };

  $scope.searchAvailability = function() {
    reservationFactory.UpdateReservationConfirm({
      reservation_id: $scope.resID,
      checkIn: $scope.newCheckinDate,
      checkOut: $scope.newCheckoutDate,
      username: $rootScope.currentUser
    }, function(data) {
      $scope.viewPart3 = true;
      $scope.availability = { avail: true, message: data.message };
      $scope.newCost = data.total_cost;
    }, function(error) {
      window.alert(error.data.message || 'Rooms are not available.');
    });
  };

  $scope.updateReservation = function() {
    reservationFactory.UpdateReservation({
      username: $rootScope.currentUser,
      reservation_id: $scope.resID,
      checkIn: $scope.newCheckinDate,
      checkOut: $scope.newCheckoutDate
    }, function() {
      $window.location.href = '#/portal';
    });
  };

  $scope.cancelReservation = function() {
    reservationFactory.CancelReservation({
      reservation_id: $scope.resID,
      username: $rootScope.currentUser
    }, function() {
      window.alert('Reservation cancelled.');
      $window.location.href = '#/portal';
    }, function(error) {
      window.alert(error.data.message || 'Could not cancel reservation.');
    });
  };

  $scope.refundAmount = function(checkinDate, cost) {
    var delta = Math.round((new Date(checkinDate) - new Date()) / 86400000);
    if (delta <= 1) {
      return 0;
    }
    if (delta < 4) {
      return cost * 0.8;
    }
    return cost;
  };

  $scope.loadCalendar();
})

.controller('reportController', function($rootScope, $scope, reportFactory, pricingFactory) {
  $scope.loggedInBool = $rootScope.alreadyLoggedIn();
  $scope.monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  $scope.getMonth = function(month) {
    return $scope.monthNames[parseInt(month, 10) - 1] || month;
  };
  $scope.location = 'Atlanta';
  $scope.room_type = 'Single';
  $scope.adjustment_percent = 0;

  reportFactory.ResReport({}, function(data) { $scope.resReport = data; });
  reportFactory.PopularRoomCatReport({}, function(data) { $scope.popCatReport = data; });
  reportFactory.RevenueReport({}, function(data) { $scope.revenueReport = data; });
  reportFactory.Confirmations({}, function(data) { $scope.confirmations = data; });
  pricingFactory.List({}, function(data) { $scope.priceRules = data; });

  reportFactory.DemandForecast({}, function(data) {
    $scope.demandForecast = data;
    setTimeout(function() {
      var canvas = document.getElementById('forecastChart');
      if (!canvas || !window.Chart) {
        return;
      }
      var atlanta = data.forecast.filter(function(item) { return item.location === 'Atlanta'; });
      new Chart(canvas, {
        type: 'bar',
        data: {
          labels: atlanta.map(function(item) { return item.month; }),
          datasets: [{ label: 'Atlanta forecast occupancy %', data: atlanta.map(function(item) { return item.predicted_occupancy; }) }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true, max: 100 } } }
      });
    }, 100);
  });

  $scope.createRule = function() {
    pricingFactory.Create({
      location: $scope.location,
      room_type: $scope.room_type,
      start_date: $scope.start_date,
      end_date: $scope.end_date,
      adjustment_percent: $scope.adjustment_percent
    }, function() {
      pricingFactory.List({}, function(data) { $scope.priceRules = data; });
      window.alert('Price rule created.');
    }, function(error) {
      window.alert(error.data.message || 'Could not create price rule.');
    });
  };
})

.controller('paymentController', function($rootScope, $scope, paymentFactory) {
  $scope.loggedInBool = $rootScope.alreadyLoggedIn();
  function refreshCards() {
    paymentFactory.GetCreditCards({ username: $rootScope.currentUser }, function(data) {
      $scope.creditCards = data;
      if (data.length > 0) {
        $scope.cardToDelete = data[0].last4;
      }
    });
  }
  refreshCards();
  $scope.addCard = function() {
    paymentFactory.AddCreditCard({
      username: $rootScope.currentUser,
      card_number: $scope.creditCardNumber,
      cvv: $scope.cvv,
      expiration_date: $scope.expirationDate,
      name: $scope.cardName
    }, function() {
      window.alert('Card successfully added.');
      refreshCards();
    }, function(error) {
      window.alert(error.data.message || 'Could not add card.');
    });
  };
  $scope.deleteCard = function() {
    paymentFactory.DeleteCreditCard({ username: $rootScope.currentUser, card_number: $scope.cardToDelete }, function() {
      window.alert('Card successfully deleted.');
      refreshCards();
    }, function(error) {
      window.alert(error.data.message || 'Could not delete card.');
    });
  };
})

.controller('reviewController', function($rootScope, $scope, reviewFactory) {
  $scope.loggedInBool = $rootScope.alreadyLoggedIn();
  $scope.location = 'Atlanta';
  $scope.rating = 'good';
  $scope.reviews = [];
  $scope.addReview = function() {
    reviewFactory.AddReview({
      location: $scope.location,
      comment: $scope.comment || '',
      rating: $scope.rating,
      username: $rootScope.currentUser
    }, function() {
      window.alert('Review added.');
    }, function(error) {
      window.alert(error.data.message || 'Could not add review.');
    });
  };
  $scope.getReviews = function() {
    reviewFactory.GetReviews({ location: $scope.location }, function(data) {
      $scope.viewPart2 = true;
      $scope.reviews = data;
      $scope.emptyTable = data.length === 0 ? 'No reviews for this location.' : '';
    });
  };
})

.config(function($routeProvider) {
  $routeProvider
    .when('/', { templateUrl: 'static/views/welcome.html' })
    .when('/login', { templateUrl: 'static/views/login.html', controller: 'loginController' })
    .when('/register', { templateUrl: 'static/views/registerUser.html', controller: 'registerController' })
    .when('/portal', { templateUrl: 'static/views/selectionPage_v2.html', controller: 'portalController' })
    .when('/searchroom', { templateUrl: 'static/views/searchRoom_v2.html', controller: 'reservationController' })
    .when('/reserve', { templateUrl: 'static/views/searchRoom_v2.html', controller: 'reservationController' })
    .when('/update', { templateUrl: 'static/views/updateReservation_v2.html', controller: 'reservationController' })
    .when('/cancel', { templateUrl: 'static/views/cancelReservation_v2.html', controller: 'reservationController' })
    .when('/payment', { templateUrl: 'static/views/payment_v2.html', controller: 'paymentController' })
    .when('/resReport', { templateUrl: 'static/views/reservationReport.html', controller: 'reportController' })
    .when('/popCatReport', { templateUrl: 'static/views/popularRoomCatReport.html', controller: 'reportController' })
    .when('/revenueReport', { templateUrl: 'static/views/revenueReport.html', controller: 'reportController' })
    .when('/demandForecast', { templateUrl: 'static/views/demandForecast.html', controller: 'reportController' })
    .when('/pricing', { templateUrl: 'static/views/pricing.html', controller: 'reportController' })
    .when('/confirmations', { templateUrl: 'static/views/confirmations.html', controller: 'reportController' })
    .when('/provideFeedback', { templateUrl: 'static/views/writeReview_v2.html', controller: 'reviewController' })
    .when('/viewFeedback', { templateUrl: 'static/views/viewFeedback_v2.html', controller: 'reviewController' });
});
