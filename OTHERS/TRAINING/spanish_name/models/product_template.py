from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    spanish_name = fields.Char('Spanish Name', default='spanish')
