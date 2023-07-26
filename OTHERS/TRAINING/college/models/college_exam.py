from datetime import date
from odoo import fields, models, api


class CollegeExam(models.Model):
    """ Model for storing Exam details... """

    _name = "college.exam"
    _description = 'exam'
    _inherit = 'mail.thread'

    @api.depends('college.class')
    def _depends_load_class_id(self):
        """ To load existing clss in M2O [class_id] from college.class..."""
        for record in self.env['college.class'].search([]):
            self.write({
                'class_id': [fields.Command.link(record.id)]
            })

    @api.onchange('type', 'name', 'semester', 'course')
    def _onchange_compute_name(self):
        """ To compute [name] field, name= semester+course+exam_type """
        self.name = " "
        if self.type and self.class_id:
            self.name = str(self.semester) + " " + str(
                self.type) + " Examination"

    @api.onchange('type', 'class_id')
    def _onchange_load_papers_ids(self):
        """ To list subjects only if the exam type is 'semester' """
        self.write({'papers_ids': [fields.Command.clear()]})
        if self.type == "Semester":
            for record in self.class_id.semester_id.syllabus_ids:
                if self.semester == record.semester_id.name:
                    self.write({
                        'papers_ids': [fields.Command.link(record.id)]
                    })

    @api.onchange('class_id')
    def _onchange_compute_valuation(self):
        """ compute valuation count in [smart button].."""
        self.valuation = self.env['college.students'].search_count(
            [('class_id', '=', self.class_id.id)])

    name = fields.Char('name', readonly=True)
    type = fields.Selection([
        ('UnitTest', 'Unit Test',),
        ('Internal', 'Internal'),
        ('Semester', 'Semester')
    ], required=True)
    class_id = fields.Many2one('college.class', 'Class', required=True)
    semester = fields.Char('Semester', related='class_id.semester_id.name',
                           store=True)
    course = fields.Char('Course', related='class_id.course', store=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', default=date.today())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('complete', 'Complete')
    ], default='draft')
    papers_ids = fields.One2many('semester.syllabus', 'exam_id', 'Papers')
    valuation = fields.Integer()
    mark_list_ids = fields.One2many('mark.list', 'exam_id')

    def _exam_state(self):
        """ Scheduled action method for change the state of examination
         to 'COMPLETED' after the examination [end_date] is over """
        if self.end_date:
            if self.end_date < date.today():
                self.state = 'complete'

    @api.onchange('end_date')
    def _onchange_compute_state(self):
        """ exam state change to completed after end_date is over...
            [scheduled action] """
        for rec in self:
            if rec.end_date < date.today():
                rec.state = 'complete'
            else:
                rec.state = 'draft'

    def open_valuation(self):
        """ To list students details by smart button [valuation]... """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exam Valuation',
            'view_mode': 'tree',
            'res_model': 'college.students',
            'domain': [('class_id', '=', self.class_id.id)],
        }

    def open_generate_mark(self):
        """ To generate mark list of students by GENERATE MARK LIST button,
            - if there is student available in the class then create mark list
            - creating mark.list and mark.details models and passing data to it.
        """
        for check in self:
            if check.class_id.students_ids.admission_no_id:
                data = []
                for record in check.papers_ids:
                    data.append({
                        'subject': record.subject,
                        'max_mark': record.max_mark,
                        'pass_mark': record.pass_mark,
                    })
                arr = []
                for item in data:
                    arr.append(fields.Command.create(item))
                if not check.mark_list_ids:
                    for rec in check.class_id.students_ids.admission_no_id:
                        check.mark_list_ids.create({
                            'student_name': rec.first_name,
                            'exam': check.name,
                            'student_class': check.class_id.name,
                            'course': check.course,
                            'semester': check.semester,
                            'exam_id': check.id,
                            'mark_ids': arr,
                        })
            check.ensure_one()
            return {
                'type': 'ir.actions.act_window',
                'name': 'Mark list',
                'view_mode': 'tree,form',
                'res_model': 'mark.list',
                'domain': [('exam_id', '=', check.id)]
            }
