# -*- coding: utf-8 -*-
{
    'name': 'Paytrail Payment',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Payment',
    'summary': """ Integrating paytrail payment gateway """,
    'description': """ This module is used to integrate 
                        paytrail payment gateway to odoo """,
    'depends': [
        'base', 'mail','payment', 'account','website','website_sale','sale',
    ],
    'data': [
        'views/payment_paytrail_templates.xml',
        'data/paytrail_provider_data.xml',
        'views/payment_provider_view.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False
}
