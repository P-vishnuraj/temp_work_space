# -*- coding: utf-8 -*-
{
    'name': 'pos_discount',
    'version': '16.0.1.0.10',
    'author': "Vishnuraj",
    'category': 'Point Of Sale',
    'description': """
                    To allow discount by dicount button in POS,
                    discount as percentage or amount decided in config of pos 
                """,
    'depends': [
        'base', 'mail', 'point_of_sale',
    ],
    'data': [
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'discount/static/src/xml/OrderlineDiscountString.xml',
            'discount/static/src/xml/OrderlineDiscountButton.xml',
            'discount/static/src/js/OrderlineDiscountButton.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}
