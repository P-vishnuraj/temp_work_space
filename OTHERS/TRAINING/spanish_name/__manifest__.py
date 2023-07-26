{
    'name': 'Spanish Name',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Others',
    'description': """ To show spanish names of products in product view and receipt """,
    'depends': [
        'base', 'mail', 'point_of_sale',
    ],
    'data': [
        'views/product_template_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'spanish_name/static/src/xml/spanish_name.xml',
            'spanish_name/static/src/js/spanish_name.js',
        ],
        # 'web.assets_frontend': [
        #     'spanish_name/static/src/js/spanish_name.js',
        # ],

    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
