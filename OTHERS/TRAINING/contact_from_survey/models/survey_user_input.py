# -*- coding: utf-8 -*-
from odoo import models


class SurveyUserInput(models.Model):
    """ model for storing user inputs of survey """
    _inherit = "survey.user_input"

    def _mark_done(self):
        """ method which is called when the last submit button works,
            inherit and added code to create new res.partner record
            based on user input """
        result_list = {}
        for line in self.user_input_line_ids:
            field_name, user_input = False, False
            if line.answer_type and line.answer_type != 'suggestion':
                field_name = line.survey_id.contact_relation_ids.search(
                    [('question_id', '=', line.question_id.id)]).contact_field
                user_input = line.mapped(eval('"value_" + line.answer_type'))[0]
            elif line.answer_type == 'suggestion':
                field_name = line.survey_id.contact_relation_ids.search(
                    [('question_id', '=', line.question_id.id)]).contact_field
                user_input = line.suggested_answer_id.value
            if field_name and user_input:
                result_list.update({field_name: user_input})
        self.env['res.partner'].create(result_list)
        return super(SurveyUserInput,self)._mark_done()
