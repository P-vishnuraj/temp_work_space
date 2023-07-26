from odoo import fields, models, api


class CollegeClass(models.Model):
    """ Model for storing class details... """

    _name = "college.class"
    _description = "class details"
    _inherit = 'mail.thread'

    @api.onchange('semester_id', 'academic_year')
    def _onchange_calc_name(self):
        """ Calculate name field of college_class..."""
        if self.semester_id and self.academic_year:
            self.name = str(self.semester_id.name) + "-" + str(
                self.academic_year)

    @api.onchange('semester_id', 'academic_year')
    def _onchange_list_students(self):
        """ Add students details Class form, from college.students model """
        if self.semester_id and self.course and self.academic_year:
            for rec in self.students_ids:
                self.write({'students_ids': [fields.Command.unlink(rec.id)]})
            for record in self.env['college.students'].search([]):
                if (
                        str(record.admission_no_id.academic_year)
                        == self.academic_year) and (
                        record.admission_no_id.course_id.name == self.course):
                    self.write({
                        'students_ids': [fields.Command.link(record.id)]
                    })

    name = fields.Char(default=_onchange_calc_name, string='Class',
                       readonly=True, required=True)
    semester_id = fields.Many2one('college.semester', 'Semester', required=True)
    course = fields.Char('Course', related='semester_id.course_id.name')
    academic_year = fields.Char('Academic year', required=True)
    students_ids = fields.One2many('college.students', 'class_id', 'Students')
    promotion_class_id = fields.Many2one('college.class', 'Promotion Class')
    _sql_constraints = [
        ('name', 'UNIQUE(name)', "The class is already created"),
    ]
