# -*- coding: utf-8 -*-
{
    'name': 'POS Clear Order Lines',
    'version': '16.0.1.0.10',
    'author': "Vishnuraj",
    'category': 'Point Of Sale',
    'summary': 'POS clear and clear all order lines',
    'description': """
                    To allow remove selected ordelines using 'x' and also able 
                    to clear all orderlines from product screen using a button 
                  """,
    'depends': [
        'base', 'mail', 'point_of_sale',
    ],
    'assets': {
        'point_of_sale.assets': [
            'clear_orderline/static/src/xml/ClearButtons.xml',
            'clear_orderline/static/src/js/OrderLineRemove.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}
