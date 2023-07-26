from odoo import fields, models, api, _


class GraduatedPlan(models.Model):
    """ model for storing graduated plan commission (One2Many) """
    _name = 'graduated.plan'

    commission_id = fields.Many2one('commission.plan')
    sequence = fields.Integer('sl.no')
    amount_from = fields.Integer('Amount from', help="if amount_from given and amount to is 0 then the amount to is taken as greater than amount_from value")
    amount_to = fields.Integer('Amount to', help="if amount_from given and amount to is 0 then the amount to is taken as greater than amount_from value")
    rate = fields.Integer('Rate%')

