// Clash of Clans Base Finder Angular App

var cocfinderApp = angular.module('cocfinderApp', []);

cocfinderApp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);

cocfinderApp.controller('cocfinderCtrl', function($scope, $http) {
    $http.get('/trophyleagues/').success(function(data) {
        $scope.trophy_leagues = data
    });
    $http.get('/townhalllevels/').success(function(data) {
        $scope.townhall_levels = data;
    });
    $http.get('/stats/avg').success(function(data) {
        $scope.avg_stats = data;
    });
});

