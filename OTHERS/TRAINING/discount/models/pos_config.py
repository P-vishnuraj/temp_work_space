""" module for add discount in both percent or amount using a button in pos """
from odoo import fields, models


class PosConfig(models.Model):
    """ model inherit and add discount and type to pos.config """
    _inherit = 'pos.config'

    discount = fields.Boolean("Discount",
        help="choose discount is based on amount or percentage "
             "ie, entering from this shop")
    discount_type = fields.Selection([
        ('amount', 'Amount'), ('percentage', 'Percentage')],
        default="amount"
    )
