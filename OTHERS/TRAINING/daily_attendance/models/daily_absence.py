import base64
from pytz import utc
from datetime import datetime, date, time
from odoo import fields, models


class DailyAbsence(models.Model):
    """ Model for daily absence... """
    _name = "daily.absence"
    _inherit = "mail.thread"
    _rec_name = "absentee_name"

    employee = fields.Many2one('hr.employee')
    absentee_name = fields.Char('Employee')
    emp_dept = fields.Char('Department')
    absent_date = fields.Date('Absent on')

    def cron_update_daily_absence(self):
        """ cron job method for compute absentees of firm,
            -computes daily absentees
            -if absentees marked previously then compute remaining days
            absence based on attendance of employees
            also send email to their managers ie, mentioning they are absent
        """
        from_date = datetime.combine(date.today(), time.max).replace(tzinfo=utc)
        to_date = datetime.combine(date.today(), time.min).replace(tzinfo=utc)
        total_work_days = self.env.user.company_id.resource_calendar_id.\
            _get_resources_day_total(from_date, to_date)
        work_days = list(dict(total_work_days[0]).keys())
        list_absentees_set = []
        last_working_day = self.env['daily.absence'].search([])[-1].absent_date
        if date.today() == work_days[0] and date.today() != last_working_day:
            present_emp = self.env['hr.attendance'].search([]).mapped(
                'employee_id.id')
            for emp in self.env['hr.employee'].search([]):
                if emp.id not in present_emp:
                    result = self.create({
                        'employee': emp.id,
                        'absentee_name': emp.name,
                        'emp_dept': emp.department_id.name,
                        'absent_date': date.today(),
                    })
                    if not list_absentees_set:
                        list_absentees_set.append({emp.parent_id: list(result)})
                    else:
                        flag = 1
                        for set in list_absentees_set:
                            if list(set.keys())[0] == result.employee.parent_id:
                                list(set.values())[0].append(result)
                                flag = 0
                        if flag == 1:
                            list_absentees_set.append(
                                {emp.parent_id: list(result)})
        for absentee_set in list_absentees_set:
            absentee = list(absentee_set.values())[0]
            if list(absentee_set.keys())[0].work_email:
                data = {
                    'absentees': absentee,
                }
                absence_report = self.env.ref(
                    'daily_attendance.action_absence_report')
                data_record = base64.b64encode(
                    self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                        absence_report, [self.id], data=data)[0])
                ir_values = {
                    'name': date.today(),
                    'type': 'binary',
                    'datas': data_record,
                    'store_fname': data_record,
                    'mimetype': 'application/pdf',
                    'res_model': 'daily.absence',
                }
                absence_report_attachment_id = self.env[
                    'ir.attachment'].sudo().create(ir_values)
                email_template = self.env.ref(
                    'daily_attendance.email_absentees')
                email_values = {
                    'email_to': list(absentee_set.keys())[0].work_email,
                    'email_from': self.env.user.email,
                }
                email_template.attachment_ids = [
                    (4, absence_report_attachment_id.id)]
                email_template.send_mail(
                    self.id, email_values=email_values, force_send=True)
                email_template.attachment_ids = [(5, 0, 0)]
