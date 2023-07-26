# -*- coding: utf-8 -*-
{
    'name': 'Absence',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Attendance',
    'description': """ To create daily absentees list as tree view default group by date and it and automatically generate everyday """,
    'depends': [
        'base', 'mail', 'hr_attendance',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/scheduled_action_absentee_data.xml',
        'views/daily_absence_view.xml',
        'views/menu.xml',
    ],
    'license': 'LGPL-3',

    'installable': True,
    'auto_install': False
}
