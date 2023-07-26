# -*- coding: utf-8 -*-
#############################################################################
#
#
#
#############################################################################
from odoo import fields, models, api, _


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('paytrail', "Paytrail")],
        ondelete={'paytrail': 'set default'}
    )
    paytrail_merchant_id = fields.Char(string='Merchant ID')
    paytrail_secret_key = fields.Char(string='Secret Key')

    # @api.model
    # def _get_payment_method_information(self):
    #     res = super()._get_payment_method_information()
    #     res['mfatoorah'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
    #     return res
    #
    # def _myfatoorah_get_api_url(self):
    #     """ Return the API URL according to the provider state.
    #     Note: self.ensure_one()
    #     :return: The API URL
    #     :rtype: str
    #     """
    #     self.ensure_one()
    #
    #     if self.state == 'enabled':
    #         return 'https://api.myfatoorah.com/'
    #     else:
    #         return 'https://apitest.myfatoorah.com/'
