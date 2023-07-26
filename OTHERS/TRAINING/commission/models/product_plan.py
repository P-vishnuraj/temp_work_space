from odoo import fields, models, api


class ProductPlan(models.Model):
    """ model for One2many of product wise commission """
    _name = 'product.plan'

    commission_id = fields.Many2one('commission.plan')
    prod_category_id = fields.Many2one('product.category', 'Category')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    percent = fields.Integer('% of rate')
    max_amount = fields.Integer('Maximum amount')

    @api.onchange('prod_category_id')
    def _onchange_category(self):
        """ for filtering product M2O field based on category """
        category = self.env['product.category'].search([('parent_path', 'like', self.prod_category_id.parent_path)])
        print(category)
        res = {'domain': {'product_id': [('categ_id', 'in', category.ids)]}}
        return res
