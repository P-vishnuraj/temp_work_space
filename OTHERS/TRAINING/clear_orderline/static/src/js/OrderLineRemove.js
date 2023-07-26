/** @odoo-module */
import Orderline from 'point_of_sale.Orderline';
import Registries from 'point_of_sale.Registries';
import OrderSummary from 'point_of_sale.OrderSummary';
//extending Orderline to add new function _clear_Line which removes single line when X button clicked...
const MyOrderline = (Orderline) => class MyOrderline extends Orderline{
    _clearLine(){
        this.env.pos.selectedOrder.orderlines.remove(this.props.line);
    }
}
//extending order summery to add _clearAll function to remove all lines when clear all button clicked...
const MyOrderSummary = (OrderSummary) => class MyOrderSummary extends OrderSummary{
    _clearAll(){
        this.env.pos.selectedOrder.orderlines.reset();
    }
}
Registries.Component.extend(Orderline, MyOrderline);
Registries.Component.extend(OrderSummary, MyOrderSummary);
