from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    category_ids = fields.Many2many(
        'product.public.category', string='Category')
    product_ids = fields.Many2many('product.template', string='Products')
