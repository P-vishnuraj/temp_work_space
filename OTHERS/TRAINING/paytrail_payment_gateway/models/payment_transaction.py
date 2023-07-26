from odoo import fields, models
from werkzeug import urls


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of `payment` to return AsiaPay-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`.

        :param dict processing_values: The generic and specific processing values of the
                                       transaction.
        :return: The dict of provider-specific processing values.
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'paytrail':
            return res

        base_url = self.provider_id.get_base_url()
        # The lang is taken from the context rather than from the partner because it is not required
        # to be logged in to make a payment, and because the lang is not always set on the partner.
        lang = self._context.get('lang') or 'en_US'
        rendering_values = {
            'merchant_id': self.provider_id.asiapay_merchant_id,
            'amount': self.amount,
            'reference': self.reference,
            'currency_code': 'USD',
            'mps_mode': 'SCP',
            'return_url': urls.url_join(base_url, '/payment/asiapay/return'),
            'payment_type': 'N',
            'language': 'en',
            'payment_method': 'ALL',
        }
        rendering_values.update({
            'secure_hash': self.provider_id._asiapay_calculate_signature(
                rendering_values, incoming=False
            ),
            # 'api_url': self.provider_id._asiapay_get_api_url()
            'api_url': 'https://www.paydollar.com/b2c2/eng/payment/payForm.jsp'
        })
        # print("rending values:...", rendering_values)
        return rendering_values
