# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Neethu UM (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import fields, models


class CrmInherits(models.Model):
    """declared new fields to this model"""
    _inherit = 'crm.lead'

    hs_object_id = fields.Char(
        string="Hubspot ID",
        help="Hubspot ID associated with this record."
    )
    sync_mode = fields.Selection(
        [
            ('import', 'HS Imported'),
            ('export', 'HS Exported'),
        ],
        string='Sync Mode',
        help="Sync mode for the record."
    )


class CrmStageInherits(models.Model):
    """declared new fields to crm_stage"""
    _inherit = 'crm.stage'

    hs_stage = fields.Char(
        string="HubSpot Stage Name",
        help="The name of the stage in HubSpot associated with this record."
    )
