""" Module for load newly created field spanish_name in pos """
from odoo import models


class PosSession(models.Model):
    """ model for inherit PosSession to load product field """
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """ supering the method and loading newly created filed spanish_name """
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['spanish_name'])
        return result
