from odoo import fields, models, api


class AccountMove(models.Model):
    """ model for adding commission details in invoice...
        -will add commission amount of sales person from the current invoice under the sales person on other info page
        -call the compute function of total commission plan in sales team member page """
    _inherit = 'account.move'

    person_commission = fields.Monetary("Salesperson Commission", compute='_compute_person_commission', store=True)

    @api.depends('payment_state', 'ref')
    def _compute_person_commission(self):
        """ computes sales persons commission amount from current invoice based on the sales persons commission plan """
        for record in self:
            record.person_commission = 0
            if record.invoice_user_id and record.payment_state == 'paid':
                for rec in record.env['crm.team.member'].search([('user_id', '=', record.invoice_user_id.id)]):
                    # print(rec.commission_plan_id)
                    commission = 0
                    if rec.commission_plan_id.from_date and rec.commission_plan_id.to_date:
                        start_date = rec.commission_plan_id.from_date
                        end_date = rec.commission_plan_id.to_date
                    else:
                        start_date = False
                        end_date = False

                    if rec.commission_plan_id.plan_type == "revenue" and rec.commission_plan_id.revenue_type == "straight":
                        total = 0
                        if start_date and end_date:
                            if record.move_type == "out_invoice":
                                if record.invoice_date:
                                    if start_date < record.invoice_date < end_date:
                                        total = record.amount_total
                        else:
                            total = record.amount_total
                        commission = total * (rec.commission_plan_id.percent / 100)
                        record.person_commission = commission
                        rec._compute_commission()

                        return

                    if rec.commission_plan_id.plan_type == "revenue" and rec.commission_plan_id.revenue_type == "graduated":
                        total = 0
                        if start_date and end_date:
                            if record.move_type == "out_invoice" and record.invoice_date and start_date < record.invoice_date < end_date:
                                        total = record.amount_total
                        else:
                            total = record.amount_total

                        for plan in rec.commission_plan_id.graduated_ids:
                            if plan.rate:
                                if plan.amount_to == 0 and plan.amount_from:
                                    if total > plan.amount_from:
                                        commission += (total-plan.amount_from) * (plan.rate / 100)
                                        total = plan.amount_from

                                if plan.amount_from < total < plan.amount_to:
                                    amnt = total - plan.amount_from
                                    commission += amnt * (plan.rate / 100)
                                    total -= amnt

                                if plan.amount_to == total:
                                    commission += (total - plan.amount_from) * (plan.rate / 100)
                                    total = plan.amount_from
                        record.person_commission = commission
                        rec._compute_commission()

                    if rec.commission_plan_id.plan_type == "product":
                        if rec.commission_plan_id.product_wise_ids.product_id:
                            # if record.move_type == 'out_invoice':
                            for plan in rec.commission_plan_id.product_wise_ids:
                                for line in record.env['account.move.line'].search(
                                        [('display_type', '=', 'product')]):
                                    if start_date and end_date:
                                        if record.invoice_date:
                                            if start_date < record.invoice_date < end_date:
                                                if line.move_id.id == record.id and plan.product_id in line.product_id:
                                                    if (line.price_subtotal * (
                                                            plan.percent / 100)) < plan.max_amount:
                                                        commission += line.price_subtotal * (plan.percent / 100)
                                                    else:
                                                        commission += plan.max_amount
                                    else:
                                        if line.move_id.id == record.id and plan.product_id in line.product_id:
                                            if (line.price_subtotal * (plan.percent / 100)) < plan.max_amount:
                                                commission += line.price_subtotal * (plan.percent / 100)
                                            else:
                                                commission += plan.max_amount
                            record.person_commission = commission
                            rec._compute_commission()
