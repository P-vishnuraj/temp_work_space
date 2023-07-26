from datetime import date
from odoo import fields, models, api


class CollegeStudents(models.Model):
    """ Model for storing students details in college..."""
    _name = "college.students"
    _description = "Students Details Fields"
    _rec_name = 'first_name'
    _inherit = 'mail.thread'

    admission_no_id = fields.Many2one('college.admission', 'Admission No',
                                      required=True)
    admission_date = fields.Date('Admission Date')
    first_name = fields.Char('First Name', related='admission_no_id.first_name',
                             required=True, readonly=False)
    last_name = fields.Char('Last Name', related='admission_no_id.last_name',
                            readonly=False)
    fathers_name = fields.Char('Fathers Name',
                               related='admission_no_id.fathers_name',
                               readonly=False)
    mothers_name = fields.Char('Mothers Name',
                               related='admission_no_id.mothers_name',
                               readonly=False)
    communication_address = fields.Text('Communication Address',
                                        related='admission_no_id'
                                                '.communication_address',
                                        readonly=False)
    same_as = fields.Boolean('Same as Above', related='admission_no_id.same_as',
                             readonly=False)
    permanent_address = fields.Text('Permanent Address',
                                    related='admission_no_id.permanent_address',
                                    readonly=False)
    phone_no = fields.Char('Phone No', related='admission_no_id.phone_no',
                           readonly=False)
    email = fields.Char('Email', related='admission_no_id.email', required=True,
                        readonly=False)
    class_id = fields.Many2one('college.class')

    _sql_constraints = [
        ('unique_admission_no', 'UNIQUE(admission_no_id)',
         "The admission number already assigned"),
    ]

    # === ONCHANGE METHODS === #
    @api.onchange("admission_no_id")
    def _onchange_admission_date(self):
        """ setting current date to 'admission_date on changing admission_no'"""
        self.admission_date = date.today()

    # === ACTION METHODS === #
    def sent_mail(self):
        """ [SENT BY MAIL] button Action to sent mail student
            with admission details... """
        mail_template = self.env.ref('college.email_admission_details')
        mail_template.send_mail(self.id, force_send=True)
