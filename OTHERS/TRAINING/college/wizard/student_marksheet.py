from odoo import fields, models
from odoo.exceptions import ValidationError
from datetime import date
from odoo.tools import date_utils
import json
import io
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class StudentMarksheet(models.TransientModel):
    """ model for wizard to get filter and condition option for the report,
        ie, based on this model data are going to filter """
    _name = 'student.marksheet'
    _description = 'Student Marksheet'

    radio = fields.Selection([('student', 'Student wise'), ('class', 'Class wise')], "Type", default='student')
    student_id = fields.Many2one('college.students', 'Student')
    class_id = fields.Many2one('college.class', 'Class')
    semester_id = fields.Many2one('college.semester', 'Semester')
    exam_id = fields.Many2one('college.exam', 'exam')

    def action_print_report(self):
        """ method to call pass data from wizard """
        data = {
            'radio': self.radio,
            'student': self.student_id.first_name,
            'class': self.class_id.id,
            'semester': self.semester_id.name,
            'exam': self.exam_id.id,
        }
        if self.radio == "student":
            return self.env.ref('college.action_student_marksheet_report').report_action(None, data=data)
        else:
            return self.env.ref('college.action_student_class_report').report_action(None, data=data)

    def action_print_excel_report(self):
        """ Action method for button print excel report
            pass data from wizard model"""
        data = {
            'radio': self.radio,
            'student': self.student_id.first_name,
            'class': self.class_id.id,
            'semester': self.semester_id.name,
            'exam': self.exam_id.id,
        }
        st_lines = self.student_query(data)
        cl_lines = self.class_query(data)
        if (self.radio == 'student' and st_lines) or (self.radio == 'class' and cl_lines):
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'student.marksheet',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Excel Report',
                         'radio': self.radio,
                         },
                'report_type': 'xlsx',
            }

    def student_query(self, data):
        """ method to do queries for student wise excel report """
        query = f"SELECT id FROM mark_list "
        if not (data['exam'] or data['semester'] or data['student']):
            pass

        if data['exam'] and data['semester'] and data['student']:
            query += f"WHERE " \
                     f"exam_id = {data['exam']} " \
                     f"AND semester = '{data['semester']}' " \
                     f"AND student_name = '{data['student']}'"

        elif data['exam'] and data['semester']:
            query += f"WHERE " \
                     f"exam_id = {data['exam']} " \
                     f"AND semester = '{data['semester']}'"

        elif data['exam'] and data['student']:
            query += f"WHERE " \
                     f"exam_id = {data['exam']} " \
                     f"AND student_name = '{data['student']}'"

        elif data['student'] and data['semester']:
            query += f"WHERE " \
                     f"student_name = '{data['student']}' " \
                     f"AND semester = '{data['semester']}'"

        elif data['exam']:
            query += f"WHERE " \
                     f"exam_id = {data['exam']}"

        elif data['semester']:
            query += f"WHERE " \
                     f"semester = '{data['semester']}'"

        elif data['student']:
            query += f"WHERE " \
                     f"student_name = '{data['student']}'"

        self.env.cr.execute(query)
        rec_list = [i[0] for i in self.env.cr.fetchall()]
        lines = self.env['mark.list'].browse(rec_list)

        if not lines:
            print("not")
            raise ValidationError("No Data is available")
        else:
            return lines

    def get_xlsx_student_report(self, data, response):
        """ To manipulate and print student wise report data to excel file
            based on queries """

        lines = self.student_query(data)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        # === Cell format ===#
        head1 = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '14px'})
        head2 = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '10px'})
        head4 = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '10px',
             'bg_color': '#ccccb3'})
        head3 = workbook.add_format(
            {'align': 'right', 'bold': False, 'font_size': '10px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})

        # === Company details === #
        sheet.merge_range(f'G1:I1', self.env.user.company_id.name, head3)
        sheet.merge_range(f'G2:I2', self.env.user.partner_id.street, head3)
        sheet.merge_range(f'G3:I3', self.env.user.partner_id.city, head3)
        sheet.merge_range(f'G4:I4', self.env.user.partner_id.zip, head3)
        sheet.merge_range(f'G5:I5', str(date.today()), head3)

        # === Header details === #
        h = 6
        for line in lines:
            sheet.merge_range(f'D{h}:G{h}', line.student_name +
                              "'s Mark Sheet", head1)
            sheet.merge_range(f'D{h + 1}:G{h + 1}', line.course + "-" +
                              line.exam_id.class_id.academic_year, head2)
            sheet.write(f'B{h + 2}', "EXAM:", txt)
            sheet.merge_range(f'C{h + 2}:E{h + 2}', line.exam, txt)
            sheet.write(f'B{h + 3}', "RESULT:", txt)
            if line.pass_fail:
                sheet.write(f'C{h + 3}', "PASS", txt)
            else:
                sheet.write(f'C{h + 3}', "FAIL", txt)

            # === Table Heading === #
            sheet.merge_range(f'B{h + 5}:C{h + 5}', "SUBJECT", head4)
            sheet.merge_range(f'D{h + 5}:E{h + 5}', "MARK", head4)
            sheet.merge_range(f'F{h + 5}:G{h + 5}', "PASS MARK", head4)
            sheet.merge_range(f'H{h + 5}:I{h + 5}', "PASS / FAIL", head4)

            # === Table Rows === #
            i = 1
            for mark in line.mark_ids:
                sheet.merge_range(f'B{h + 5 + i}:C{h + 5 + i}',
                                  mark.subject, txt)
                sheet.merge_range(f'D{h + 5 + i}:E{h + 5 + i}', mark.mark, txt)
                sheet.merge_range(f'F{h + 5 + i}:G{h + 5 + i}',
                                  mark.pass_mark, txt)
                if mark.pass_fail:
                    sheet.merge_range(f'H{h + 5 + i}:I{h + 5 + i}', "PASS", txt)
                else:
                    sheet.merge_range(f'H{h + 5 + i}:I{h + 5 + i}', "FAIL", txt)
                i += 1
            h += (i + 7)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def class_query(self, data):
        """ method to do queries for class wise excel report """
        query = f"SELECT id FROM college_exam "
        if not (data['exam'] or data['semester'] or data['class']):
            pass

        if data['exam'] and data['semester'] and data['class']:
            query += f"WHERE " \
                     f"college_exam.id = {data['exam']} " \
                     f"AND college_exam.semester = '{data['semester']}' " \
                     f"AND college_exam.class_id = {data['class']}"

        elif data['exam'] and data['semester']:
            query += f"WHERE " \
                     f"college_exam.id = {data['exam']} " \
                     f"AND college_exam.semester = '{data['semester']}'"

        elif data['exam'] and data['class']:
            query += f"WHERE " \
                     f"college_exam.id = {data['exam']} " \
                     f"AND college_exam.class_id = {data['class']}"

        elif data['class'] and data['semester']:
            query += f"WHERE " \
                     f"college_exam.class_id = {data['class']} " \
                     f"AND college_exam.semester = '{data['semester']}'"

        elif data['exam']:
            query += f"WHERE " \
                     f"college_exam.id = {data['exam']}"

        elif data['semester']:
            query += f"WHERE " \
                     f"college_exam.semester = '{data['semester']}'"

        elif data['class']:
            query += f"WHERE " \
                     f"college_exam.class_id = '{data['class']}'"

        self.env.cr.execute(query)
        rec_list = [i[0] for i in self.env.cr.fetchall()]
        lines = self.env['college.exam'].browse(rec_list)
        if not lines:
            raise ValidationError("No Data is available")

        return lines

    def get_xlsx_class_report(self, data, response):
        """ To manipulate and print class wise report data to excel file
            based on queries """

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        lines = self.class_query(data)

        # === Cell format ===#
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head1 = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '14px'})
        head2 = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '10px'})
        head3 = workbook.add_format(
            {'align': 'right', 'bold': False, 'font_size': '10px'})
        head4 = workbook.add_format(
            {'align': 'right', 'bold': False, 'font_size': '10px',
             'bg_color': '#ccccb3'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        txt2 = workbook.add_format({'font_size': '10px', 'align': 'centre'})
        sheet.set_column(0, 10, 15)

        # === Company details === #
        sheet.merge_range(f'F1:G1', self.env.user.company_id.name, head3)
        sheet.merge_range(f'F2:G2', self.env.user.partner_id.street, head3)
        sheet.merge_range(f'F3:G3', self.env.user.partner_id.city, head3)
        sheet.merge_range(f'F4:G4', self.env.user.partner_id.zip, head3)
        sheet.merge_range(f'F5:G5', str(date.today()), head3)

        # === Header details === #
        h = 6
        for line in lines:
            sheet.merge_range(f'C{h}:F{h}', line.class_id.name + " Mark Sheet",
                              head1)
            sheet.merge_range(f'C{h + 1}:F{h + 1}', line.course + "-" +
                              line.class_id.academic_year, head2)
            sheet.write(f'B{h + 3}', "EXAM:", txt)
            sheet.merge_range(f'C{h + 3}:D{h + 3}', line.name, txt)
            count = 0
            passed = 0
            failed = 0
            for m in line.mark_list_ids:
                if m.pass_fail:
                    passed += 1
                else:
                    failed += 1
                count += 1
            sheet.write(f'B{h + 4}', "TOTAL:", txt)
            sheet.merge_range(f'C{h + 4}:D{h + 4}', count, txt)
            sheet.write(f'B{h + 5}', "PASS:", txt)
            sheet.merge_range(f'C{h + 5}:D{h + 5}', passed, txt)
            sheet.write(f'B{h + 6}', "FAIL:", txt)
            sheet.merge_range(f'C{h + 6}:D{h + 6}', failed, txt)
            sheet.write(f'B{h + 7}', "RATIO:", txt)
            sheet.merge_range(f'C{h + 7}:D{h + 7}', str(passed / count * 100) +
                              "%", txt)

            # === Table Heading === #
            sheet.write(h+8, 1, "STUDENT", head4)
            a = 2
            for sub in line.mark_list_ids[0].mark_ids:
                sheet.write(h+8, a, sub.subject, head4)
                a += 1
            sheet.write(h+8, a, "OBTAINED MARK", head4)
            sheet.write(h+8, a+1, "TOTAL MARK", head4)
            sheet.write(h+8, a+2, "PASS / FAIL", head4)

            # === Table Rows === #
            i = h + 9
            for ml in line.mark_list_ids:
                sheet.write(i, 1, ml.student_name, txt)
                a = 2
                gt = 0
                for mark in ml.mark_ids:
                    sheet.write(i, a, mark.mark, txt)
                    a += 1
                    gt += mark.max_mark
                sheet.write(i, a, ml.total, txt)
                sheet.write(i, a+1, gt, txt)
                if ml.pass_fail:
                    sheet.write(i, a+2, "PASS", txt)
                else:
                    sheet.write(i, a+2, "FAIL", txt)
                i += 1
            h += (i+1)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
