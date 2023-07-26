odoo.define('top_customers.carousel_snippet', function(require) {
    'use strict';
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;

    var Dynamic = PublicWidget.Widget.extend({
        selector: '.dynamic_snippet_blog',
        willStart: async function() {
            await rpc.query({
                route: '/top_customers',
            }).then((data) => {
                this.data = data;
            });
        },
    start: function() {
        var chunks = _.chunk(this.data, 4)
        chunks[0].is_active = true
        this.$el.find('#carousel').html(
            qweb.render('top_customers.top_10_snippet_carousel', {chunks})
        )
    },
});
PublicWidget.registry.dynamic_snippet_blog = Dynamic;
return Dynamic;
});
