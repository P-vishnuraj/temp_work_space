# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SurveyContact(models.Model):
    """ model for contact relation page in survey.survey """
    _name = 'survey.contact'
    _description = 'survey contact'

    def _get_contact_fields(self):
        """ method for return all fields in res.partner """
        contact_fields = self.env['res.partner'].fields_get().items()
        return [(key, value['string']) for key, value in contact_fields
                if value['type'] == 'char' and value['searchable']]

    survey_contact_id = fields.Many2one('survey.survey',
                                        string='Survey Contact')
    sequence = fields.Integer('Sequence')
    question_id = fields.Many2one('survey.question', required=True,
                                  ondelete='cascade')
    contact_field = fields.Selection(_get_contact_fields,
                                     string='Contact Field', required='true')

    @api.onchange('question_id')
    def _onchange_question_id_values(self):
        return {'domain': {
            'question_id': [('survey_id', 'in', self.survey_contact_id.ids),
                            ('id', 'not in',
                             self.survey_contact_id.contact_relation_ids.question_id.ids)]}}
