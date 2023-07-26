# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    float_field = fields.Float("Float field")
