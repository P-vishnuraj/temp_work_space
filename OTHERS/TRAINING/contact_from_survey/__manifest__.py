# -*- coding: utf-8 -*-
{
    'name': 'Contact From Survey',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'survey',
    'summary': """ creating contact from survey """,
    'description': """ To create contact when user submit contact fields
                        details using survey questions """,
    'depends': [
        'base', 'mail', 'survey',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_survey_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False
}
