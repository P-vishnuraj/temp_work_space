{
    'name': 'Material Request',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Material',
    'description': """ 
                    """,
    'depends': [
        'base', 'mail', 'product', 'purchase', 'stock',
    ],

    'data': [
        'data/ir_sequence_data.xml',
        'security/material_request_security.xml',
        'security/ir.model.access.csv',
        'views/material_request_view.xml',
        'views/menu.xml',
    ],
    'license': 'LGPL-3',

    'installable': True,
    'application': True,
    'auto_install': False
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
