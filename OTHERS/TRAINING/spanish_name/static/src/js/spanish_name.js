/** @odoo-module */
import { Orderline } from 'point_of_sale.models';
import Registries from 'point_of_sale.Registries';
//extending Orderline to add new value to Pos Receipt...
const MyOrderline = (Orderline) => class MyOrderline extends Orderline{
    export_for_printing(){
//    method for adding key value to the receipt
        var result = super.export_for_printing(...arguments);
        result['spanish_name'] = this.product.spanish_name
        return result;
    }
}
Registries.Model.extend(Orderline, MyOrderline);
