from odoo import fields, models, api


class CommissionPlan(models.Model):
    """ model for commission plan """
    _name = "commission.plan"
    _inherit = 'mail.thread'

    name = fields.Char('Plan name', required=True)
    activate = fields.Boolean('Activate')
    from_date = fields.Date('Available from')
    to_date = fields.Date('to')
    plan_type = fields.Selection([
        ('product', 'Product wise'),
        ('revenue', 'Revenue wise'),
    ], 'Plan type', required=True)
    product_wise_ids = fields.One2many('product.plan', 'commission_id', 'Product wise Plan')
    revenue_type = fields.Selection([
        ('straight', 'Straight'),
        ('graduated', 'Graduated')
    ], 'Revenue type', default='straight')
    graduated_ids = fields.One2many('graduated.plan', 'commission_id', 'Graduated plan')
    percent = fields.Integer("Commission %")
