from odoo import fields, models, api


class ProductReference(models.Model):
    """ model for product reference
        - for one2many field in material.request"""
    _name = "product.reference"

    material_req_id = fields.Many2one('material.request')
    product_id = fields.Many2one('product.template', 'material')
    is_po = fields.Boolean('Get by PO', help="if not purchase order, it'll be considered as internal transfer")
    transfer_from_id = fields.Many2one('stock.location', 'Source', compute='_depend_is_po', store=True, inverse='_inverse_is_po')
    transfer_to_id = fields.Many2one('stock.location', 'Destination', compute='_depend_is_po', store=True, inverse='_inverse_is_po')

    @api.depends('is_po')
    def _depend_is_po(self):
        for rec in self:
            if not rec.is_po:
                loc = self.env['stock.location'].search([('complete_name', '=', 'WH/Stock')])
                rec.write({
                    'transfer_from_id': loc.id,
                    'transfer_to_id': loc.id
                })
            else:
                self.transfer_from_id = False
                self.transfer_to_id = False

    def _inverse_is_po(self):
        """ inverse method to make computed locations editable... """
        pass
