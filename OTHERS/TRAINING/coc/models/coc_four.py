from odoo import api, fields, models, _


class CocFour(models.Model):
    """ Model for coc4
    """

    _name = "coc.four"
    _inherit = 'mail.thread'
    _description = "coc4"

    status = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')])
class ResPartner(models.Model):
    _inherit = 'res.partner'

    coc_field = fields.Char(string='New field')

