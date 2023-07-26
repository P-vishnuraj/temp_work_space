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
import datetime
from odoo import fields, models, _
from odoo.exceptions import ValidationError
from hubspot import HubSpot
from hubspot.crm.deals import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException


class HubSpotAuth(models.Model):
    """New model for hubspot connector to set up the credentials"""
    _name = 'hubspot.connector'
    _description = 'HubSpot Connector'

    name = fields.Char(string="Instance Name", help="name of the instance")
    access_key = fields.Char(string="Access Key",
                             help="This key is used to connect the hubspot with odoo"
                             )
    import_contacts = fields.Boolean(string="Import Contacts",
                                     help="This will enable import of contact from hubspot to odoo"
                                     )
    export_contacts = fields.Boolean(string="Export Contacts",
                                     help="This will enable export of contact from odoo to hubspot"
                                     )
    import_company = fields.Boolean(string="Import Company",
                                    help="This will enable import of companies from hubspot to odoo"
                                    )
    export_company = fields.Boolean(string="Export Company",
                                    help="This will enable export of companies from Odoo to HubSpot"
                                    )
    export_deals = fields.Boolean(string="Export Deals",
                                  help="This will enable export of deals from odoo to hubspot"
                                  )
    import_deals = fields.Boolean(string="Import Deals",
                                  help="This will enable import of deals from hubspot to odoo"
                                  )
    owner_id = fields.Char(string="Owner ID",
                           required=True,
                           help="This is used to export the deals")
    last_import_date = fields.Datetime(string="Last Import Date",
                                       readonly=True,
                                       help="This is the last imported time")
    last_export_date = fields.Datetime(string="Last Export Date",
                                       readonly=True,
                                       help="This is the last exported time"
                                       )
    last_import_date_company = fields.Datetime(string="Last Import Date",
                                               readonly=True,
                                               help="This is the last imported time"
                                               )
    last_export_date_company = fields.Datetime(string="Last Export Date",
                                               readonly=True,
                                               help="This is the last exported time"
                                               )
    last_import_deal_date = fields.Datetime(string="Last Import Date",
                                            readonly=True,
                                            help="This is the last imported time"
                                            )
    last_export_deal_date = fields.Datetime(string="Last Export Date",
                                            readonly=True,
                                            help="This is the last exported time"
                                            )

    def import_hubspot_partner(self):
        """Import contacts from Hubspot"""
        api_client = HubSpot(access_token=self.access_key)
        all_contacts = api_client.crm.contacts.get_all()
        partners = self.env['res.partner'].search([])
        for rec in all_contacts:
            exist = partners.search([('hs_object_id', '=', rec.properties['hs_object_id'])])
            if not exist:
                #  create contact if no existing records found
                self.env['res.partner'].sudo().create({
                    'name': rec.properties['firstname'] + '' + rec.properties['lastname']
                    if rec.properties['lastname'] else rec.properties['firstname'],
                    'email': rec.properties['email'],
                    'hs_object_id': rec.properties['hs_object_id'],
                    'sync_mode': 'import'
                })
            else:
                # update the records
                exist.write({
                    'name': rec.properties['firstname'] + '' + rec.properties['lastname']
                    if rec.properties['lastname'] else rec.properties['firstname'],
                    'email': rec.properties['email'],
                    'hs_object_id': rec.properties['hs_object_id'],
                    'sync_mode': 'import'
                })
        # hubspot log
        self.env['hubspot.sync.history'].sudo().create({
            'date': fields.datetime.now(),
            'res_model_id': self.env.ref('base.model_res_partner').id,
            'sync_mode': 'import',
            'state': 'success',
            'count': len(all_contacts),
        })
        self.last_import_date = datetime.datetime.now()

    def _update_or_create_contact(self, rec):
        """update or create contacts"""
        api_client = HubSpot(access_token=self.access_key)
        properties = {
            "email": rec.email,
            "firstname": rec.name,
            "lastname": "",
            "phone": rec.phone,
            "website": rec.website
        }
        simple_public_object_input = SimplePublicObjectInput(properties=properties)
        if rec.hs_object_id:
            # update existing contact
            api_client.crm.contacts.basic_api.update(
                contact_id=rec.hs_object_id,
                simple_public_object_input=simple_public_object_input
            )
        else:
            # create new contact
            api_response = api_client.crm.contacts.basic_api.create(
                simple_public_object_input=simple_public_object_input
            )
            if api_response:
                rec.hs_object_id = api_response.properties['hs_object_id']

    def action_export_partner(self):
        """Export Contacts from Odoo to Hubspot"""
        try:
            existing_contacts = self.env['res.partner'].search([('hs_object_id', '!=', False)])
            updated_count = sum(
                [self._update_or_create_contact(rec) for rec in existing_contacts]
            )

            new_contacts = self.env['res.partner'].search([('hs_object_id', '=', False)])
            sum(
                [self._update_or_create_contact(rec) for rec in new_contacts]
            )
            self.env['hubspot.sync.history'].create({
                'date': fields.datetime.now(),
                'res_model_id': self.env.ref('base.model_res_partner').id,
                'sync_mode': 'export',
                'state': 'success',
                'count': len(new_contacts) + updated_count,
            })

            self.last_export_date = fields.datetime.now()
        except ApiException as exception:
            self.env['hubspot.sync.history'].create({
                'date': fields.datetime.now(),
                'res_model_id': self.env.ref('base.model_res_partner').id,
                'sync_mode': 'export',
                'state': 'error',
                'error': exception.body,
            })
            raise ValidationError(
                _(f"Exception when creating company: {exception}\n")
            ) from exception

    def action_import_company(self):
        """Import company"""
        api_client = HubSpot(access_token=self.access_key)
        all_companies = api_client.crm.companies.get_all()
        company = self.env['res.company'].search([])
        for rec in all_companies:
            already_exist = company.search([('hs_object_id', '=', rec.properties['hs_object_id'])])
            if not already_exist:
                # create if no existing records fount
                company.sudo().create({
                    'name': rec.properties['name'],
                    'hs_object_id': rec.properties['hs_object_id'],
                    'sync_mode': 'import',
                    'website': rec.properties['domain']
                })
            else:
                # update if record already exist
                already_exist.sudo().write({
                    'name': rec.properties['name'],
                    'hs_object_id': rec.properties['hs_object_id'],
                    'sync_mode': 'import',
                    'website': rec.properties['domain']
                })
        self.env['hubspot.sync.history'].sudo().create({
            'date': fields.datetime.now(),
            'res_model_id': self.env.ref('base.model_res_company').id,
            'sync_mode': 'import',
            'state': 'success',
            'count': len(all_companies),
        })
        self.last_import_date_company = datetime.datetime.now()

    def _update_or_create_company(self, rec):
        """Update or create companies"""
        api_client = HubSpot(access_token=self.access_key)
        properties = {
            "city": rec.city,
            "domain": rec.website,
            "industry": "",
            "name": rec.name,
            "phone": rec.phone,
        }
        simple_public_object_input = SimplePublicObjectInput(properties)
        if rec.hs_object_id:
            api_client.crm.companies.basic_api.update(
                company_id=rec.hs_object_id,
                simple_public_object_input=simple_public_object_input
            )
        else:
            api_client.crm.companies.basic_api.create(
                simple_public_object_input=simple_public_object_input
            )

    def action_export_company(self):
        """Export companies"""
        try:
            existing_company = self.env['res.company'].search([('hs_object_id', '!=', False)])
            updated_count = sum(
                self._update_or_create_company(rec) for rec in existing_company
            )
            new_company = self.env['res.company'].search([('hs_object_id', '=', False)])
            sum(self._update_or_create_company(rec) for rec in new_company)
            self.env['hubspot.sync.history'].create({
                'date': fields.datetime.now(),
                'res_model_id': self.env.ref('base.model_res_company').id,
                'sync_mode': 'export',
                'state': 'success',
                'count': len(new_company) + updated_count,
            })
            self.last_export_date = fields.datetime.now()
        except ApiException as exception:
            self.env['hubspot.sync.history'].sudo().create({
                'date': fields.datetime.now(),
                'res_model_id': self.env.ref('base.model_res_company').id,
                'sync_mode': 'export',
                'state': 'error',
                'reason': exception,
            })
            raise ValidationError(_(
                f"Exception when creating company: {exception}\n"
            )) from exception

    def action_import_deals(self):
        """Import Deals"""
        api_client = HubSpot(access_token=self.access_key)
        all_deals = api_client.crm.deals.get_all()
        crm = self.env['crm.lead']
        hs_id_set = set(crm.search([]).mapped('hs_object_id'))
        hs_stages = {
            stage.hs_stage: stage.id for stage in self.env['crm.stage'].search(
                [('hs_stage', '!=', False)]
            )
        }
        deals_to_create = []
        deals_to_write = []
        for rec in all_deals:
            hs_object_id = rec.properties['hs_object_id']
            if hs_object_id in hs_id_set:
                # Update existing deal
                deals_to_write.append((hs_object_id, {
                    'name': rec.properties['dealname'] or 'Lead',
                    'expected_revenue': rec.properties['amount'],
                    'stage_id': hs_stages.get(rec.properties['dealstage']),
                    'date_deadline': rec.properties['closedate'],
                    'sync_mode': 'import',
                }))
            else:
                # Create new deal
                deals_to_create.append({
                    'name': rec.properties['dealname'] or 'Lead',
                    'hs_object_id': hs_object_id,
                    'expected_revenue': rec.properties['amount'],
                    'stage_id': hs_stages.get(rec.properties['dealstage']),
                    'date_deadline': rec.properties['closedate'],
                    'sync_mode': 'import',
                })

        if deals_to_write:
            for hs_object_id, properties in deals_to_write:
                crm.browse(
                    crm.search([('hs_object_id', '=', hs_object_id)])
                ).sudo().write(properties)
        if deals_to_create:
            crm.sudo().create(deals_to_create)

        self.env['hubspot.sync.history'].sudo().create({
            'date': datetime.datetime.now(),
            'res_model_id': self.env.ref('crm.model_crm_lead').id,
            'sync_mode': 'import',
            'state': 'success',
            'count': len(all_deals),
        })
        self.last_import_deal_date = datetime.datetime.now()

    def action_export_deals(self):
        """Export Deals"""
        api_client = HubSpot(access_token=self.access_key)
        try:
            deals = self.env['crm.lead'].search([('hs_object_id', '=', False)])
            for rec in deals:
                properties = {
                    "amount": rec.expected_revenue,
                    "closedate": rec.date_deadline if rec.date_deadline else '',
                    "dealname": rec.name,
                    "hubspot_owner_id": self.owner_id,
                    "pipeline": "default"
                }
                simple_public_object_input = SimplePublicObjectInput(properties)
                api_response = api_client.crm.deals.basic_api.create(
                    simple_public_object_input=simple_public_object_input
                )
                if api_response:
                    rec.write({
                        'hs_object_id': api_response.properties['hs_object_id'],
                        'sync_mode': 'export'
                    })
            self.last_export_deal_date = datetime.datetime.now()
        except ApiException as exception:
            self.env['hubspot.sync.history'].sudo().create({
                'date': datetime.datetime.now(),
                'res_model_id': self.env.ref('crm.model_crm_lead').id,
                'sync_mode': 'export',
                'state': 'error',
                'reason': exception,
            })
            raise ValidationError(_(
                f"Exception when creating company: {exception}\n"
            )) from exception
