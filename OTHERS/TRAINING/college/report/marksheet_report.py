from odoo import models
from odoo.exceptions import ValidationError


class MarksheetReport(models.AbstractModel):
    """ model for print student wise data """
    _name = 'report.college.report_marksheet_template'

    def _get_report_values(self, doc_ids, data=None):
        """ Retrieve data using query and pass values to QWEB """

        query = f"""select mark_list.id, mark_list.exam, 
                mark_list.student_name,
                 mark_list.course, mark_list.semester, 
                mark_list.pass_fail, college_class.academic_year 
                from mark_list inner join college_exam on 
                mark_list.exam_id = college_exam.id 
                inner join college_class 
                on college_exam.class_id = 
                college_class.id """
        if not (data['exam'] or data['semester'] or data['student']):
            pass
        if data['exam'] and data['semester'] and data['student']:
            query += f"""WHERE 
                     mark_list.exam_id = {data['exam']} 
                     AND mark_list.semester = '{data['semester']}' 
                     AND mark_list.student_name = '{data['student']}'"""
        elif data['exam'] and data['semester']:
            query += f"""WHERE 
                     mark_list.exam_id = {data['exam']} 
                     AND mark_list.semester = '{data['semester']}'"""
        elif data['exam'] and data['student']:
            query += f"""WHERE 
                     mark_list.exam_id = {data['exam']} 
                     AND mark_list.student_name = '{data['student']}'"""
        elif data['student'] and data['semester']:
            query += f"""WHERE 
                     mark_list.student_name = '{data['student']}' 
                     AND mark_list.semester = '{data['semester']}'"""
        elif data['exam']:
            query += f"""WHERE 
                     mark_list.exam_id = {data['exam']}"""
        elif data['semester']:
            query += f"""WHERE 
                     mark_list.semester = '{data['semester']}'"""
        elif data['student']:
            query += f"""WHERE 
                     mark_list.student_name = '{data['student']}'"""
        self.env.cr.execute(query)
        lines = self.env.cr.dictfetchall()
        query1 = f"""select mark_details.subject, mark_details.mark, 
                 mark_details.pass_mark, mark_details.pass_fail, 
                 mark_details.marklist_id from mark_details where 
                 mark_details.marklist_id in (select mark_list.id 
                 from mark_list)"""
        self.env.cr.execute(query1)
        details = self.env.cr.dictfetchall()
        if not lines:
            raise ValidationError("No Data is available")
        return {
            'lines': lines,
            'details': details,
        }
