# -*- coding: utf-8 -*-
{
    'name': 'PO Migration',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Others',
    'summary': """ Fetching purchase orders from v15 to v16 """,
    'description': """ To fetch all purchase orders created in the old database
                        ie in version 15.0 to the new database in version 16.0
                    """,
    'depends': [
        'base', 'mail', 'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/migration_details_view.xml',
        'wizard/migrate_purchase_view.xml',
        'views/menu.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False
}
