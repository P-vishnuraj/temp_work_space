from odoo import fields, models


class PromotionClass(models.Model):
    """ Model for storing Promoted students details of exams..."""
    _name = "promotion.class"
    _description = "promotion"
    _inherit = 'mail.thread'
    _rec_name = 'exam_id'

    exam_id = fields.Many2one('college.exam', 'Exam')
    class_id = fields.Many2one('college.class')
    semester = fields.Char('Semester', related='exam_id.semester')
    promoted_students_ids = fields.One2many('mark.list', 'promotion_id')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('complete', 'Complete')
    ], default='pending')
    generated = fields.Boolean(default=False)

    def action_generate_promotion(self):
        """ Button [generate promotion] action
            -lists the students who are passed for the selected exam"""
        self.generated = True
        for record in self.env['mark.list'].search([]):
            if record.pass_fail \
                    and record.exam_id == self.exam_id \
                    and record.student_class == self.class_id.name:
                self.write(
                    {'promoted_students_ids': [fields.Command.link(record.id)]})

    def action_promote_students(self):
        """ Button [promote] action
            -it converts the students to promotion class of their current class
        """
        for record in self.env['mark.list'].search([]):
            if record.pass_fail and record.exam_id == self.exam_id \
                    and record.student_class == self.class_id.name:
                for stud_rec in self.env['college.students'].search([]):
                    if stud_rec.admission_no_id.first_name \
                            == record.student_name:
                        if stud_rec.class_id.promotion_class_id:
                            stud_rec.class_id =\
                                stud_rec.class_id.promotion_class_id
                            # self.state = 'complete'
        self.state = 'complete'
