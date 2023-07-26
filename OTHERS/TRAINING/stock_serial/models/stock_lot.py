from odoo import fields, models, api, _


class StockLot(models.Model):
    """ model for inherit stock.lot model """
    _inherit = "stock.lot"

    def action_import_doc(self):
        wizard = self.env['file.wizard'].create({ })
        return {
            'name': _('UPLOAD LOT/SERIAL NO.'),
            'type': 'ir.actions.act_window',
            'res_model': 'file.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new'
        }
