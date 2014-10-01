jQuery(function () {
    var body = jQuery('body');
    var timeout = null;

    var ajax = function (id) {
        window.location.hash = '#' + id;
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
                id: id
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
                refresh(id);
            },
            function (jqXHR, textStatus, errorThrown) {
                overlay.addClass('hide');
                spinner.addClass('hide');
                failure_1.removeClass('hide');
                refresh(id);
            }
        );
    };

    var refresh = function (id) {
        timeout = window.setTimeout(function () {
            ajax(id);
        }, 30000);
    };

    jQuery('th input[type="checkbox"]').click(function(){
        var $this = jQuery(this);
        $this.closest('table').find('td input[type="checkbox"]').prop(
            'checked', $this.is(':checked')
        );
    });

    if (!!body.attr('data-background'))
        jQuery.backstretch(body.attr('data-background'));

    jQuery('.nav li a[data-id]').click(function () {
        jQuery('.tweet').remove();
        window.clearTimeout(timeout);
        var $this = jQuery(this);
        jQuery('.nav li').removeClass('active');
        $this.parent().addClass('active');
        ajax($this.attr('data-id'));
    });

    var id = window.location.hash.substr(1);
    if (id.length) {
        jQuery('.nav li a[data-id="' + id + '"]').click();
    } else {
        jQuery('.nav li a[data-id]:first').click();
    }
    jQuery(window).scroll(function() {
        var w = jQuery(window).scrollTop();
        if (w >= jQuery('header nav').height())
            jQuery('header nav').addClass('small');
        else
            jQuery('header nav').removeClass('small');
    });
    export_results(jQuery('#export-results'));
});

var export_results = function(elements){
    elements.click(function(){
        var visitors = {};
        var url = jQuery(this).attr('data-url');
        var table = jQuery(this).parent().parent().find('table');
        jQuery.each(table.find('tr:not(:first)'), function(index_) {
            visitors[index_] = new Array();
            jQuery.each(jQuery(this).find('td:not(:first)'), function(index) {
                visitors[index_].push(jQuery(this).text().trim());
            });
        });
        visitors = JSON.stringify(visitors);
        var form = [
            '<form action="'+url+'" id="export" method="post" style="display:none;">',
            '<input name="csrf_token" type="hidden"/>',
            '<input name="visitors" type="hidden"/>',
            '</form>'
        ];
        form = form.join('');
        jQuery('body').append(form);
        form = jQuery('#export');
        form.find('[name="csrf_token"]').val(jQuery(this).parent().parent().find('[name="csrf_token"]').val());
        form.find('[name="visitors"]').val(visitors);
        form.submit();
        form.remove();
        return false;
    });
};
