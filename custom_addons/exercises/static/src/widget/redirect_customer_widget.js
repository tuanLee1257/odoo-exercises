odoo.define('exercises.redirect_customer_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var field_registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');

    var _t = core._t;

    var CustomURLWidget = AbstractField.extend({
        className: 'redirect_to_customer',
        supportedFieldTypes: ['char'],

        /**
         * Hiển thị giá trị trong widget
         *
         * @private
         */
        _render: function () {
            this.$el.empty();

            var url = this.value;
            var text = url ? url : _t('No URL');

            // Tạo một đối tượng liên kết URL
            var link = $('<a>', {
                href: url,
                text: text,
                target: '_blank',
                readonly: this.nodeOptions.readonly, // Áp dụng thuộc tính readonly
            });

            this.$el.append(link);
        },
    });

    field_registry.add('custom_url', CustomURLWidget);

    return CustomURLWidget;
});
