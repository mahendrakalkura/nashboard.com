jQuery(function () {
    var body = jQuery('body');
    var neighborhood_id = jQuery('.top [name="neighborhood_id"]');
    var timeout = null;

    var ajax = function (category_id) {
        window.location.hash = '#' + category_id;
        var dashboard = jQuery('#dashboard');
        var tweets = dashboard.find('#tweets');
        var failure_1 = dashboard.find('#failure_1');
        var failure_2 = dashboard.find('#failure_2');
        var overlay = jQuery('#overlay');
        var spinner = jQuery('#spinner');
        failure_1.addClass('hide');
        failure_2.addClass('hide');
        overlay.removeClass('hide');
        spinner.removeClass('hide');
        jQuery.ajax({
            cache: false,
            data: {
                category_id: category_id,
                neighborhood_id: neighborhood_id.val()
            },
            timeout: 30000,
            type: 'POST',
            url: dashboard.attr('data-url')
        }).then(
            function (data, textStatus, jqXHR) {
                overlay.addClass('hide');
                spinner.addClass('hide');
                jQuery(
                    jQuery(data).find('.tweet').get().reverse()
                ).each(function () {
                    var $this = jQuery(this);
                    if (tweets.find(
                        '.tweet[data-id="' + $this.attr('data-id') + '"]'
                    ).length) {
                        return;
                    }
                    $this.find('.created_at').timeago();
                    tweets.prepend($this);
                });
                if (!tweets.find('.tweet').length) {
                    failure_2.removeClass('hide');
                }
                refresh(category_id);
            },
            function (jqXHR, textStatus, errorThrown) {
                overlay.addClass('hide');
                spinner.addClass('hide');
                failure_1.removeClass('hide');
                refresh(category_id);
            }
        );
    };

    var handles_ajax = function (category_id) {
        window.location.hash = '#' + category_id;
        var dashboard = jQuery('#dashboard');
        var tweets = dashboard.find('#tweets');
        var failure_1 = dashboard.find('#failure_1');
        var failure_2 = dashboard.find('#failure_2');
        var overlay = jQuery('#overlay');
        var spinner = jQuery('#spinner');
        failure_1.addClass('hide');
        failure_2.addClass('hide');
        overlay.removeClass('hide');
        spinner.removeClass('hide');
        jQuery.ajax({
            cache: false,
            data: {
                category_id: category_id,
                neighborhood_id: neighborhood_id.val()
            },
            timeout: 30000,
            type: 'POST',
            url: dashboard.attr('data-url')
        }).then(
            function (data, textStatus, jqXHR) {
                overlay.addClass('hide');
                spinner.addClass('hide');
                jQuery(
                    jQuery(data).find('.tweet').get().reverse()
                ).each(function () {
                    var $this = jQuery(this);
                    if (tweets.find(
                        '.tweet[data-id="' + $this.attr('data-id') + '"]'
                    ).length) {
                        return;
                    }
                    $this.find('.created_at').timeago();
                    tweets.prepend($this);
                });
                if (!tweets.find('.tweet').length) {
                    failure_2.removeClass('hide');
                }
                handles_refresh(category_id);
            },
            function (jqXHR, textStatus, errorThrown) {
                overlay.addClass('hide');
                spinner.addClass('hide');
                failure_1.removeClass('hide');
                handles_refresh(category_id);
            }
        );
    };

    var refresh = function (category_id) {
        timeout = window.setTimeout(function () {
            ajax(category_id);
        }, 30000);
    };

    var handles_refresh = function (category_id) {
        timeout = window.setTimeout(function () {
            handles_ajax(category_id);
        }, 30000);
    };

    jQuery('th input[type="checkbox"]').click(function(){
        var $this = jQuery(this);
        $this.closest('table').find('td input[type="checkbox"]').prop(
            'checked', $this.is(':checked')
        );
    });

    jQuery(window).scroll(function() {
        var w = jQuery(window).scrollTop();
        if (w >= jQuery('header nav').height()) {
            jQuery('header nav').addClass('small');
        } else {
            jQuery('header nav').removeClass('small');
        }
    });

    if (!!body.attr('data-background')) {
        jQuery.backstretch(body.attr('data-background'));
    }

    if (jQuery('#dashboard').length) {
        jQuery('.nav li a[data-id]').click(function () {
            jQuery('.tweet').remove();
            window.clearTimeout(timeout);
            var $this = jQuery(this);
            jQuery('.nav li').removeClass('active');
            $this.parent().addClass('active');
            ajax($this.attr('data-id'));
            handles_ajax($this.attr('data-id'));

            //hide the navbar after click
            if (jQuery('.navbar-toggle').css('display') != 'none' && jQuery('.navbar-collapse').hasClass('in'))
                jQuery('.navbar-toggle').click();

            return false;
        });

        jQuery('.top [name="neighborhood_id"]').change(function () {
            var id = window.location.hash.substr(1);
            if (id.length) {
                jQuery('.nav li a[data-id="' + id + '"]').click();
            } else {
                jQuery('.nav li a[data-id]:first').click();
            }
            return false;
        }).change();
    }
    jQuery('#summary').wysihtml5();
});
