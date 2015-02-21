var application = angular.module('application', []);

application.config(function ($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $interpolateProvider.startSymbol('[!').endSymbol('!]');
});

application.controller('dashboard', [
    '$attrs',
    '$http',
    '$rootScope',
    '$scope',
    '$timeout',
    function ($attrs, $http, $rootScope, $scope, $timeout) {
        $rootScope.neighborhood = true;

        $rootScope.overlay = false;
        $rootScope.spinner = false;

        $scope.mode = 'real_time';

        $scope.tweets = [];

        $scope.failure_1 = false;
        $scope.failure_2 = false;

        $scope.refresh = function () {
            $rootScope.overlay = true;
            $rootScope.spinner = true;
            $http({
                data: jQuery.param({
                    mode: $scope.mode,
                    neighborhood_id: $scope.neighborhood_id
                }),
                method: 'POST',
                url: $attrs.urlRefresh
            }).
            error(function (data, status, headers, config) {
                $rootScope.overlay = false;
                $rootScope.spinner = false;

                $scope.tweets = [];

                $scope.failure_1 = true;
                $scope.failure_2 = false;

                $timeout($scope.refresh, 10000);
            }).
            success(function (data, status, headers, config) {
                $rootScope.overlay = false;
                $rootScope.spinner = false;

                $scope.tweets = data.tweets;

                $scope.failure_1 = false;
                $scope.failure_2 = false;

                if (!$scope.tweets.length) {
                    $scope.failure_1 = false;
                    $scope.failure_2 = true;
                }

                $timeout($scope.refresh, 60000);
            });
        };

        $scope.vote = function (tweet, direction) {
            $http({
                data: jQuery.param({
                    direction: direction,
                    tweet_id: tweet.id
                }),
                method: 'POST',
                url: $attrs.urlVote
            }).
            success(function (data, status, headers, config) {
                tweet.vote = direction;
            });
        };


        $scope.$watch('neighborhood_id', function (new_value, old_value) {
            $scope.refresh();
        }, true);

        $scope.$watch('mode', function (new_value, old_value) {
            $scope.refresh();
        }, true);

        $scope.refresh();
    }
]);

application.controller('handles', [
    '$attrs',
    '$http',
    '$rootScope',
    '$scope',
    '$timeout',
    function ($attrs, $http, $rootScope, $scope, $timeout) {
        $rootScope.overlay = false;
        $rootScope.spinner = false;

        $scope.tweets = [];

        $scope.failure_1 = false;
        $scope.failure_2 = false;

        $scope.refresh = function () {
            $rootScope.overlay = true;
            $rootScope.spinner = true;
            $http({
                method: 'POST',
                url: $attrs.url
            }).
            error(function (data, status, headers, config) {
                $rootScope.overlay = false;
                $rootScope.spinner = false;

                $scope.tweets = [];

                $scope.failure_1 = true;
                $scope.failure_2 = false;

                $timeout($scope.refresh, 10000);
            }).
            success(function (data, status, headers, config) {
                $rootScope.overlay = false;
                $rootScope.spinner = false;

                $scope.tweets = data.tweets;

                $scope.failure_1 = false;
                $scope.failure_2 = false;

                if (!$scope.tweets.length) {
                    $scope.failure_1 = false;
                    $scope.failure_2 = true;
                }

                $timeout($scope.refresh, 60000);
            });
        };

        $scope.refresh();
    }
]);

application.directive('tweet', function () {
    return {
        link: function (scope, element, attr) {
            scope.$watch('tweet', function (new_value, old_value) {
                jQuery(element).find('.created_at').timeago();
            });
        },
        restrict: 'A'
    };
});

application.filter('html', function ($sce) {
    return function (html) {
        return $sce.trustAsHtml(html);
    };
});

jQuery(function () {
    jQuery(window).scroll(function() {
        var w = jQuery(window).scrollTop();
        if (w >= jQuery('header nav').height()) {
            jQuery('header nav').addClass('small');
        } else {
            jQuery('header nav').removeClass('small');
        }
    });

    jQuery('th input[type="checkbox"]').click(function(){
        var $this = jQuery(this);
        $this.closest('table').find('td input[type="checkbox"]').prop(
            'checked', $this.is(':checked')
        );
    });

    jQuery('#summary').wysihtml5({
        'blockquote': true,
        'color': true,
        'emphasis': true,
        'font-styles': true,
        'html': true,
        'image': true,
        'link': true,
        'lists': true,
        'toolbar': {
            'fa': true
        }
    });

    if (!!jQuery('body').attr('data-background')) {
        jQuery.backstretch(jQuery('body').attr('data-background'));
    }
});
