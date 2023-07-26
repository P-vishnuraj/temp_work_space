{
    'name': 'CRM_Commission',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Others',
    'description': """ to create and set commission plan for employees commission """,
    'depends': [
        'base', 'mail', 'crm',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/commission_plan_view.xml',
        'views/crm_team_view.xml',
        'views/crm_team_member_view.xml',
        'views/account_move_view.xml',
        'views/menu.xml',
    ],
    'license': 'LGPL-3',

    'installable': True,
    'application': True,
    'auto_install': False
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
