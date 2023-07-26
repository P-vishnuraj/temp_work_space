from odoo import fields, models


class DailyAbsence(models.Model):
    """ Model for daily absence... """
    _name = "daily.absence"
    _inherit = "mail.thread"

    absentee_name = fields.Char('Employee')
    emp_dept = fields.Char('Department')
    absent_date = fields.Date('Absent on')

    def cron_update_absence(self):
        """ cron job method for calculate absentees of firm
            -calculates daily absentees
            -if absentees marked previously then calculate remaining days absence based on attendance of employees
        """
        present_emp = self.env['hr.attendance'].search([]).mapped('employee_id.id')
        work_days = [val.date() for val in self.env['hr.attendance'].search([]).mapped('check_out') if val]
        if self.env['daily.absence'].search([]):
            last_absent_day = self.env['daily.absence'].search([]).mapped('absent_date')[-1]
            for w_day in sorted(list(set(work_days))):
                if w_day <= last_absent_day:
                    continue
                for emp in self.env['hr.employee'].search([]):
                    if emp.id not in present_emp:
                        self.create({
                            'absentee_name': emp.name,
                            'emp_dept': emp.department_id.name,
                            'absent_date': w_day,
                        })
        else:
            for day in sorted(list(set(work_days))):
                for emp in self.env['hr.employee'].search([]):
                    if emp.id not in present_emp:
                        self.create({
                            'absentee_name': emp.name,
                            'emp_dept': emp.department_id.name,
                            'absent_date': day,
                        })
