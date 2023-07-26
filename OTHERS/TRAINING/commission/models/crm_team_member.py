from odoo import fields, models, api


class CrmTeamMember(models.Model):
    """ model for adding commission plan in crm_team_member page  """
    # _name = "crm.team.member"
    _inherit = 'crm.team.member'

    commission_plan_id = fields.Many2one('commission.plan', 'Commission Plan')
    commission_amount = fields.Float('Commission Amount', compute='_compute_commission', store=True)

    @api.depends('commission_plan_id')
    def _compute_commission(self):
        """ To calculate total commission amount of a sales person based on his commission plan """
        self.commission_amount = 0
        commission = 0
        if self.commission_plan_id.from_date and self.commission_plan_id.to_date:
            start_date = self.commission_plan_id.from_date
            end_date = self.commission_plan_id.to_date
        else:
            start_date = False
            end_date = False

        if self.commission_plan_id.plan_type == "product":
            if self.commission_plan_id.product_wise_ids.product_id:
                for inv in self.env['account.move'].search(
                        [('move_type', '=', 'out_invoice'), ('invoice_user_id.id', '=', self.user_id.id), ('payment_state', '=', 'paid')]):
                    for plan in self.commission_plan_id.product_wise_ids:
                        for line in self.env['account.move.line'].search([('display_type', '=', 'product')]):
                            if start_date and end_date:
                                if inv.invoice_date:
                                    if start_date < inv.invoice_date < end_date:
                                        if line.move_id.id == inv.id and plan.product_id in line.product_id:
                                            if (line.price_subtotal * (plan.percent / 100)) < plan.max_amount:
                                                commission += line.price_subtotal * (plan.percent / 100)
                                            else:
                                                commission += plan.max_amount
                            else:
                                if line.move_id.id == inv.id and plan.product_id in line.product_id:
                                    if (line.price_subtotal * (plan.percent/100)) < plan.max_amount:
                                        commission += line.price_subtotal * (plan.percent/100)
                                    else:
                                            commission += plan.max_amount
                self.commission_amount = commission
            return

        if self.commission_plan_id.plan_type == "revenue" and self.commission_plan_id.revenue_type == "straight":
            total = 0
            if start_date and end_date:
                for inv in self.env['account.move'].search(
                        [('move_type', '=', 'out_invoice'), ('invoice_user_id.id', '=', self.user_id.id), ('payment_state', '=', 'paid')]):
                    if inv.invoice_date:
                        if start_date < inv.invoice_date < end_date:
                            total += inv.amount_total
            else:
                total = sum(self.env['account.move'].search([('move_type', '=', 'out_invoice'), ('invoice_user_id.id', '=', self.user_id.id), ('payment_state', '=', 'paid')]).mapped('amount_total'))
            commission = total * (self.commission_plan_id.percent/100)
            self.commission_amount = commission
            return

        if self.commission_plan_id.plan_type == "revenue" and self.commission_plan_id.revenue_type == "graduated":
            total = 0
            if start_date and end_date:
                for inv in self.env['account.move'].search(
                        [('move_type', '=', 'out_invoice'), ('invoice_user_id.id', '=', self.user_id.id), ('payment_state', '=', 'paid')]):
                    if inv.invoice_date:
                        if start_date < inv.invoice_date < end_date:
                            total += inv.amount_total
            else:
                total = sum(self.env['account.move'].search(
                    [('move_type', '=', 'out_invoice'), ('invoice_user_id.id', '=', self.user_id.id), ('payment_state', '=', 'paid')]).mapped(
                    'amount_total'))

            for plan in self.commission_plan_id.graduated_ids:
                if plan.rate:
                    if plan.amount_to == 0 and plan.amount_from:
                        if total > plan.amount_from:
                            commission += (total - plan.amount_from) * (plan.rate / 100)
                            total = plan.amount_from

                    if plan.amount_from < total < plan.amount_to:
                        amnt = total - plan.amount_from
                        commission += amnt * (plan.rate / 100)
                        total -= amnt

                    if plan.amount_to == total:
                        commission += (total - plan.amount_from) * (plan.rate / 100)
                        total = plan.amount_from

            self.commission_amount = commission
