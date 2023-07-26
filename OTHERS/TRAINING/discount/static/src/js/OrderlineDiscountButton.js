odoo.define('discount.OrderlineDiscountButton', function(require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
// extending PosComponent to add Discount button in screen
    class OrderlineDiscountButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
//        on click method for the discount button
        async onClick() {
            const config = this.env.pos.config
            const selectedOrderline = this.env.pos.get_order().get_selected_orderline();
            if (!selectedOrderline) return;
            var head = (config.discount_type == "percentage") ? "Enter Discount Percentage" : "Enter Discount Amount";
            const { confirmed, payload: inputDiscount } = await this.showPopup("NumberPopup", {
                title: this.env._t(head),
            });
            if (confirmed) {
                if (config.discount_type == "percentage") {
                    selectedOrderline.discount = inputDiscount;
                    selectedOrderline.discountStr = inputDiscount;
                }
                else {
                    selectedOrderline.discountStr = Number(selectedOrderline.discountStr)+Number(inputDiscount);
                    selectedOrderline.price -= (inputDiscount / selectedOrderline.quantity)
                }
            }
        }
    }
    OrderlineDiscountButton.template = 'OrderlineDiscountButton';
//    adding the created component to product screen
    ProductScreen.addControlButton({
        component: OrderlineDiscountButton,
        condition: function() {
            return this.env.pos.config.discount;
        },
    });
    Registries.Component.add(OrderlineDiscountButton);
    return OrderlineDiscountButton;
});