from datetime import date
from odoo import http
from odoo.http import request


class WebAdmission(http.Controller):
    """ controller class for take online admission """
    @http.route(['/admission'], type='http', auth="user", website=True)
    def admission_menu(self):
        """ controller method for online admission form
            can create admission via online  """
        course = request.env['college.course'].sudo().search([])
        values = {
            'course': course,
        }
        return request.render("college.web_admission_temp", values)

    @http.route(['/admission/submit/'], type='http', auth="user", website=True)
    def admission_submit(self, **kw):
        """ controller method to create admission
            by clicking submit button"""
        if not kw['application_date']:
            kw['application_date'] = date.today()
        request.env['college.admission'].sudo().create({
            'first_name': kw['first_name'],
            'last_name': kw['last_name'],
            'fathers_name': kw['fathers_name'],
            'mothers_name': kw['mothers_name'],
            'communication_address': kw['communication_address'],
            'permanent_address': kw['permanent_address'],
            'phone_no': kw['phone_no'],
            'email': kw['email'],
            'course_id': kw['course_id'],
            'application_date': kw['application_date'],
            'academic_year': kw['academic_year'],
            'previous_qualification': kw['previous_qualification'],
            'college_name': kw['college_name'],
            'tc': kw.get('tc').read(),
        })
        return request.render("college.web_admission_success")
