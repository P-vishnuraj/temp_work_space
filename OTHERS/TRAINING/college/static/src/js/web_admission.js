odoo.define('college.example', function (require) {
    "use strict";
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;
    const publicWidget = require('web.public.widget')
    publicWidget.registry.collegeEvent = publicWidget.Widget.extend({
        selector:'.s_website_form',
        events: {
            'click .same_as': '_hide_address2',
        },
        _hide_address2: function (ev) {
            this.$('#permanent_address').toggle()
            console.log(this.$('#same_as').val())
        },
    })
});

