from odoo import fields, models, api


class MarkList(models.Model):
    """ Model for storing marklist details of students in exams..."""
    _name = "mark.list"
    _description = "Mark list"
    _inherit = 'mail.thread'
    _rec_name = 'student_name'

    @api.depends('mark_ids')
    def _compute_total(self):
        """ compute total mark of student by adding subjects marks """
        for rec in self:
            rec.total = sum(rec.mark_ids.mapped('mark'))

    @api.depends('total')
    def _compute_pass(self):
        """ compute the student is pass/fail based on subjects mark """
        for rec in self:
            rec.pass_fail = False if False in rec.mark_ids.mapped(
                'pass_fail') else True

    @api.depends('total')
    def _compute_rank(self):
        """ compute rank of student based on total marks of students
            scored in exam wise. """
        for rec in self:
            if rec.total != 0:
                list_total = self.env['mark.list'].search(
                    [('exam', '=', rec.exam)]).mapped('total')
                list_total.pop()
                list_total.append(rec.total)
                sort_total = sorted(list_total, reverse=True)
                for record in self.env['mark.list'].search(
                        [('exam', '=', rec.exam)]):
                    if record.total in sort_total:
                        record.rank = sort_total.index(record.total) + 1
                        if record.total == 0:
                            record.rank = 0

    student_name = fields.Char('Student')
    exam = fields.Char('Exam')
    student_class = fields.Char('Class')
    course = fields.Char('Course')
    semester = fields.Char('Semester')
    pass_fail = fields.Boolean('Pass', compute='_compute_pass', store=True)
    rank = fields.Integer('Rank', default=0, compute='_compute_rank',
                          store=True)
    exam_id = fields.Many2one('college.exam')
    mark_ids = fields.One2many('mark.details', 'marklist_id')
    total = fields.Float('Total Marks', default=0, compute='_compute_total',
                         store=True)
    promotion_id = fields.Many2one('promotion.class')


class MarkDetails(models.Model):
    """for One2many
        store subject wise details of students... """
    _name = 'mark.details'

    subject = fields.Char('Subject')
    mark = fields.Integer('Mark')
    max_mark = fields.Integer('Maximum mark')
    pass_mark = fields.Integer('Pass mark')
    pass_fail = fields.Boolean('Pass')
    marklist_id = fields.Many2one('mark.list')

    @api.onchange("mark")
    def _onchange_mark(self):
        """ compute each subject is pass/fail by scored mark is less than or
            greater than of pass mark of the subject in syllabus. """
        if self.mark > self.max_mark:
            self.mark = 0
            return {'warning': {
                'title': 'Validation Error',
                'message': 'The mark should be less than maximum mark',
            }}
        else:
            self.pass_fail = True if self.mark >= self.pass_mark else False
