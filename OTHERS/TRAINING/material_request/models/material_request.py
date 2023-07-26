from odoo import fields, models, api, _
from datetime import date


class MaterialRequest(models.Model):
    """ Model for storing Material requests... """
    _name = "material.request"
    _rec_name = "reference_no"
    _description = "material_request"
    _inherit = 'mail.thread'

    @api.model
    def create(self, vals):
        """ To create sequence number for material_request """
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'material.request') or _('New')
        return super(MaterialRequest, self).create(vals)

    reference_no = fields.Char(readonly=True, default='New')
    user_name_id = fields.Many2one('res.users', default=lambda self: self.env.uid, readonly=True)
    request_date = fields.Date('Request Date', default=date.today())
    material_ids = fields.One2many('product.reference', 'material_req_id')
    rfq_count = fields.Integer(default=0)
    transfer_count = fields.Integer(default=0)
    rfq_ids = fields.Many2many('purchase.order')
    transfer_ids = fields.Many2many('stock.picking')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected')
    ], default='draft')

    def action_rfq_smart(self):
        """ action for RFQ smart button """
        # print(self.rfq_ids.ids)
        return {
            'type': 'ir.actions.act_window',
            'name': 'RFQ',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('id', 'in', self.rfq_ids.ids)],
        }

    def action_transfer_smart(self):
        """ action for Internal Transfer Smart button """
        print("Internal transfer smart button")
        return {
            'type': 'ir.actions.act_window',
            'name': 'RFQ',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('id', 'in', self.transfer_ids.ids)],
        }

    def action_sent_request(self):
        """ action for sent button """
        self.state = 'sent'

    def action_confirm_request(self):
        """ action for confirm button"""
        if self.material_ids:
            self.state = 'confirm'
        else:
            print("else")
            return {'warning': {
                'title': 'Validation Error',
                'message': 'Pass mark should be less than maximum mark'
            }}

    def action_approve_request(self):
        """ Button approve for Requisition Managers """
        self.state = 'approved'

    def action_sanction_request(self):
        """ Button sanction for Requisition Head """
        self.state = 'done'
        for rec in self.material_ids:
            if rec.is_po:
                print("PO")
                for record in rec.product_id.seller_ids.partner_id:
                    rfq = self.env['purchase.order'].create({
                        'partner_id': record.id,
                        'order_line': [fields.Command.create({
                            'name': rec.product_id.name,
                            'product_id': rec.product_id.id,
                        })],
                    })
                    self.write({
                        'rfq_ids': [fields.Command.link(rfq.id)]
                    })
                    self.rfq_count += 1
            else:
                transfer = self.env['stock.picking'].create({
                    'location_id': rec.transfer_from_id.id,
                    'location_dest_id': rec.transfer_to_id.id,
                    'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                })

                self.write({
                    'transfer_ids': [fields.Command.link(transfer.id)]
                })
                self.transfer_count += 1

    def action_reject_request(self):
        """ Button sanction for Requisition Head """
        self.state = 'rejected'
