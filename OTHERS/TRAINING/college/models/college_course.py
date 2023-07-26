from odoo import fields, models


class CollegeCourse(models.Model):
    """ Model for storing course details available in college... """
    _name = "college.course"
    _description = "courses"
    _inherit = 'mail.thread'
    _rec_name = "name"

    name = fields.Char('Course Name', required=True)
    category = fields.Selection([
        ('Diploma', 'Diploma'),
        ('UG', 'UnderGraduation'),
        ('PG', 'Post Graduation')],
        required=True)
    duration = fields.Integer('Duration')
    semester_no = fields.Integer('No of Semesters')
    semester_ids = fields.One2many('college.semester', 'course_id', 'Semester')
