from odoo import fields, models, api


class CollegeSemester(models.Model):
    """ MODEL for semester details available in different courses... """
    _name = "college.semester"
    _description = "semester"
    _rec_name = "name"
    _inherit = 'mail.thread'

    name = fields.Char('Semester')
    sem_no = fields.Integer('Number of semester', required=True, default="1")
    course_id = fields.Many2one('college.course', 'Course', required=True,
                                default=" ")
    syllabus_ids = fields.One2many('semester.syllabus', 'semester_id',
                                   'Syllabus')
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', "The class already created"),
    ]

    # === ONCHANGE METHODS === #
    @api.onchange("sem_no", "course_id")
    def _onchange_compute_name(self):
        """ To compute the value of [name] field... """
        self.name = "Sem" + str(self.sem_no) + "-" + str(self.course_id.name)


class SemesterSyllabus(models.Model):
    """ MODEL for One2Many field Syllabus for [college_semester] """
    _name = "semester.syllabus"
    _description = "syllabus"

    subject = fields.Char('Subject', required=True)
    max_mark = fields.Integer('Maximum mark', required=True)
    pass_mark = fields.Integer('Pass Mark')
    semester_id = fields.Many2one('college.semester')
    exam_id = fields.Many2one('college.exam')

    @api.onchange('pass_mark', 'max_mark')
    def _onchange_pass_mark(self):
        """ on change method for popup validation error,
            when pass mark > maximum mark  """
        if self.max_mark and self.pass_mark > self.max_mark:
            self.pass_mark = 0
            return {'warning': {
                'title': 'Validation Error',
                'message': 'Pass mark should be less than maximum mark'
            }}
