from odoo import models
from odoo.exceptions import ValidationError


class ClassReport(models.AbstractModel):
    """ model for print class wise data """
    _name = 'report.college.report_class_template'

    def _get_report_values(self, doc_ids, data=None):
        """ Retrieve data using query and pass values to QWEB """

        query = f"""select college_exam.id, college_exam.name as exam_name, 
                college_exam.course, college_exam.semester, 
                college_exam.class_id, 
                college_class.name, college_class.academic_year 
                from college_exam inner join college_class on 
                college_exam.class_id = college_class.id """
        if not (data['exam'] or data['semester'] or data['class']):
            pass
        if data['exam'] and data['semester'] and data['class']:
            query += f"""WHERE 
                     college_exam.id = {data['exam']} 
                     AND college_exam.semester = '{data['semester']}' 
                     AND college_exam.class_id = {data['class']}"""
        elif data['exam'] and data['semester']:
            query += f"""WHERE 
                     college_exam.id = {data['exam']} 
                     AND college_exam.semester = '{data['semester']}'"""
        elif data['exam'] and data['class']:
            query += f"""WHERE 
                     college_exam.id = {data['exam']} 
                     AND college_exam.class_id = {data['class']}"""
        elif data['class'] and data['semester']:
            query += f"""WHERE 
                     college_exam.class_id = {data['class']} 
                     AND college_exam.semester = '{data['semester']}'"""
        elif data['exam']:
            query += f"""WHERE 
                     college_exam.id = {data['exam']}"""
        elif data['semester']:
            query += f"""WHERE 
                     college_exam.semester = '{data['semester']}'"""
        elif data['class']:
            query += f"""WHERE 
                     college_exam.class_id = '{data['class']}'"""
        self.env.cr.execute(query)
        lines = self.env.cr.dictfetchall()
        query1 = f""" select mark_list.id, mark_list.exam_id, 
        mark_list.pass_fail, mark_list.student_name, 
        mark_list.total from mark_list """
        self.env.cr.execute(query1)
        data1 = self.env.cr.dictfetchall()
        query2 = f""" select mark_details.subject, mark_details.mark, 
        mark_details.max_mark, mark_details.marklist_id
        from mark_details """
        self.env.cr.execute(query2)
        data2 = self.env.cr.dictfetchall()
        if not lines:
            raise ValidationError("No Data is available")
        return {
            'doc_ids': doc_ids,
            'doc_model': 'mark.list',
            'data': data,
            'lines': lines,
            'data1': data1,
            'data2': data2,
        }
