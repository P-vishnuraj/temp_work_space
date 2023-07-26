{
    'name': 'top_customers',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Others',
    'description': """ dynamic snippet carousel for top most buyed customers """,
    'depends': [
        'base', 'mail', 'website', 'sale_management',
    ],
    'data': [
        'views/top_customers_snippet.xml',
    ],
    'assets': {
            'web.assets_frontend': [
                'top_customers/static/src/xml/top_10_carousel.xml',
                'top_customers/static/src/js/top_customers_curousel.js',
            ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
