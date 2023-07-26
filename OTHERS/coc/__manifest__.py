# -*- coding: utf-8 -*-
{
    'name': 'COC',
    'version': '16.0.1.0.0',
    'category': 'sale_management',
    'summary': 'This module will helps to merge different types of pickings',
    'description': """This module helps to manage delivery orders and incoming 
    shipments by merge pickings""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'product', 'sale_management'],
    'data': [
        'views/sale_order_views.xml',
    ],
    # 'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False
}
