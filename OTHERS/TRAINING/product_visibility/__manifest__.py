{
    'name': 'product_visibility',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Others',
    'description': """ To limit the visibility of products/ product categories in website shop """,
    'depends': [
        'base', 'mail', 'website', 'website_sale',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
