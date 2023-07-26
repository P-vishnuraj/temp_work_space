from odoo import fields, models, api, _


class SaleOrder(models.Model):
    """ model for inherit sale.order model """
    _inherit = "sale.order"

    def action_confirm(self):
        """ method for merge same sale order lines with updated quantity """
        new_lines = []
        arr = []
        for sale_line in self.order_line:
            same_line = self.order_line.filtered(lambda m: m.product_template_id.id == sale_line.product_template_id.id and m.price_unit == sale_line.price_unit)
            new_lines.append(same_line)
        for same_rec_set in list(set(new_lines)):
            # u_price = 0
            u_price = same_rec_set[0].price_unit
            qty = 0
            for rec in same_rec_set:
                qty += rec.product_uom_qty
            same_rec_set[0].product_uom_qty = qty
            same_rec_set[0].price_unit = u_price
            arr.append(same_rec_set[0])
        self.order_line = [fields.Command.set([i.id for i in arr])]

        return super(SaleOrder, self).action_confirm()
