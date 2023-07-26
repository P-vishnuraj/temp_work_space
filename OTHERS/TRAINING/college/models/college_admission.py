from datetime import datetime, date
from odoo import api, fields, models, _


class CollegeAdmission(models.Model):
    """ Model for storing Admission details of students in college module """

    _name = "college.admission"
    _inherit = 'mail.thread'
    _description = "college admission"
    _rec_name = "reference_no"

    def year_selection(self):
        """Values for 'Academic year' field..."""
        end_year = int(datetime.strftime(datetime.today(), '%Y'))
        year = end_year - 10
        year_list = []
        while year <= end_year + 10:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    @api.model
    def create(self, vals_list):
        """To create sequence number for college_admission"""
        if vals_list.get('reference_no', _('New')) == _('New'):
            vals_list['reference_no'] = self.env['ir.sequence'].next_by_code(
                'college.admission') or _('New')
            return super(CollegeAdmission, self).create(vals_list)
    reference_no = fields.Char(readonly=True, default='New')
    first_name = fields.Char('First Name'
                             # , required=True
                             )
    last_name = fields.Char('Last Name')
    fathers_name = fields.Char('Father Name')
    mothers_name = fields.Char('Mother Name')
    communication_address = fields.Text('Communication Address')
    permanent_address = fields.Text('Permanent Address')
    same_as = fields.Boolean('Same as Above')
    phone_no = fields.Char('Phone')
    email = fields.Char('Email'
                        # , required=True
                        )
    application_date = fields.Date('Date of Application', default=date.today())
    academic_year = fields.Selection(
        year_selection,
        'Academic Year',
        default="2022",
    )
    previous_qualification = fields.Selection([
        ('HS', 'Higher Secondary'),
        ('UG', 'Under Graduate'),
        ('PG', 'Post Graduate')
    ])
    college_name = fields.Char('Name of Institution')
    tc = fields.Binary('Attach Your TC here.'
                       # , required=True
                       )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('application', 'Application'),
         ('approved', 'Approved'),
         ('done', 'Done'),
         ('rejected', 'Rejected')],
        'Status', default='draft'
    )
    course_id = fields.Many2one(
        'college.course', 'Course'
        # , required=True
    )
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    # === ACTION METHODS === #
    def confirm_action(self):
        """ CONFIRM button action to confirm admission,
            -it changes state from DRAFT to APPLICATION, APPLICATION to DONE """
        if self.state == 'application':
            self.state = 'done'
        elif self.state == 'draft':
            self.state = 'application'

        self.sale_order_id.action_confirm()

    def reject_action(self):
        """ REJECT button action to reject admission, this button should only
            visible in state 'APPLICATION' also sent email to inform that he/she
            got rejected """
        mail_template = self.env.ref('college.email_admission_rejected')
        mail_template.send_mail(self.id, force_send=True)
        if self.state == 'application':
            self.state = 'rejected'
