{
    'name': 'Lot & Serial',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Inventory',
    'description': """ To import excel file for lot and serial no. """,
    'depends': [
        'base', 'mail', 'stock',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/stock_lot_view.xml',
        'wizard/file_wizard_view.xml',
    ],
    'license': 'LGPL-3',

    'installable': True,
    'auto_install': False
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
