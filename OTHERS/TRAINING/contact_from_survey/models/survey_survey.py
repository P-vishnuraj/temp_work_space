# -*- coding: utf-8 -*-
from odoo import fields, models


class Survey(models.Model):
    """ Model for storing survey contact as one to many in survey.survey """
    _inherit = 'survey.survey'

    contact_relation_ids = fields.One2many('survey.contact',
                                           'survey_contact_id')
