# -*- coding: utf-8 -*-
{
    'name': 'Daily Attendance',
    'version': '16.0.1.0.0',
    'author': "Vishnuraj",
    'category': 'Attendances',
    'summary': """ daily attendance and absence report """,
    'description': """ To create daily absentees report and sent it to manager every day """,
    'depends': [
        'base', 'mail', 'hr_attendance', 'hr_holidays', 'resource',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/absence_mail_template.xml',
        'data/scheduled_action_daily_attendance_data.xml',
        'views/daily_absence_view.xml',
        'views/menu.xml',
        'reports/absence_report_template.xml',
        'reports/report_action.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False
}
