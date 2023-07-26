{
    'name': 'college',
    'version': '16.0.8.5.20',
    'author': "Vishnuraj",
    'category': 'Others',
    'description': """ The college management system helps Educational Institutions
                        especially colleges in various ways, such as storing data, 
                        maintaining student profiles, analyzing administrative 
                        and academic data, improving communication, and engaging students.
                        v.6.5.x: Snippet with carousel
                    """,
    'depends': [
        'base', 'mail', 'website', 'sale_management',
    ],
    'data': [
        # 'data/demo_data.xml',
        'data/mail_template_data.xml',
        'data/ir_sequence_data.xml',
        'data/scheduled_action_data.xml',
        'security/ir.model.access.csv',
        'views/college_admission_view.xml',
        'views/college_course_view.xml',
        'views/college_students_view.xml',
        'views/college_semester_view.xml',
        'views/college_class_view.xml',
        'views/mark_list_view.xml',
        'views/promotion_class_view.xml',
        'views/college_exam_view.xml',

        'wizard/student_marksheet_view.xml',
        'report/student_marksheet_templates.xml',
        'report/report_class_template.xml',
        'report/student_marksheet_reports.xml',
        'views/menus.xml',

        'views/web_admission_view.xml',
        'views/web_admission_successful.xml',
        'views/web_menu.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'college/static/src/js/action_manager.js',
            ],
            'web.assets_frontend': [
                'college/static/src/js/web_admission.js',
            ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
