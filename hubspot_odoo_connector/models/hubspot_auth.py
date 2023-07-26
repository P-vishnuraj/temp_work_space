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
from datetime import datetime, timezone
import json
import pytz
import base64
import requests
from odoo.exceptions import AccessError
from odoo import api, fields, models, _
from hubspot import HubSpot
from hubspot.crm.deals import SimplePublicObjectInput, \
    BatchInputSimplePublicObjectBatchInput


class HubspotConnector(models.Model):
    """New model for hubspot connector to set up the credentials"""
    _name = 'hubspot.connector'
    _description = 'HubSpot Connector'

    name = fields.Char(string="Instance Name", help="name of the instance")
    # API key and id
    access_key = fields.Char(string="Access Token",
                             help="This key is used to connect the hubspot with odoo",
                             password=True)
    owner_id = fields.Char(string="Owner ID",
                           required=True,
                           help="This is used to export the deals")
    connection = fields.Boolean(string="Connection",
                                help="connected to hubspot or nor")
    # Toggles for Contacts sync
    import_contacts = fields.Boolean(
        string="Import Contacts",
        help="This will enable import of contact from hubspot to odoo")
    export_contacts = fields.Boolean(
        string="Export Contacts",
        help="This will enable export of contact from odoo to hubspot")
    update_odoo_contacts = fields.Boolean(
        string="Update Odoo Contacts",
        help="This will update contact in odoo from hubspot data")
    update_hub_contacts = fields.Boolean(
        string="Update Hubspot Contacts",
        help="This will update contact in hubspot from odoo data")
    # Toggles for Company sync
    import_company = fields.Boolean(
        string="Import Company",
        help="This will enable import of companies from hubspot to odoo")
    export_company = fields.Boolean(
        string="Export Company",
        help="This will enable export of companies from Odoo to HubSpot")
    update_odoo_company = fields.Boolean(
        string="Update Odoo Company",
        help="This will update company in odoo from hubspot data")
    update_hub_company = fields.Boolean(
        string="Update Hubspot Company",
        help="This will update company in hubspot from odoo data")
    # Toggles for Deals sync
    export_deals = fields.Boolean(
        string="Export Deals",
        help="This will enable export of deals from odoo to hubspot")
    import_deals = fields.Boolean(
        string="Import Deals",
        help="This will enable import of deals from hubspot to odoo")
    update_odoo_deals = fields.Boolean(
        string="Update Odoo Deals",
        help="This will update deals in odoo from hubspot data")
    update_hub_deals = fields.Boolean(
        string="Update Hubspot Deals",
        help="This will update deals in hubspot from odoo data")
    # Toggles for Invoices sync
    export_invoices = fields.Boolean(
        string="Export Invoices",
        help="This will enable export of invoices from odoo to hubspot")
    import_invoices = fields.Boolean(
        string="Import Invoices",
        help="This will enable import of invoices from hubspot to odoo")

    # Contacts last sync Time
    contacts_last_imported = fields.Datetime(
        string="Last Import Date", readonly=True,
        help="This is the last imported time")
    contacts_last_exported = fields.Datetime(
        string="Last Export Date", readonly=True,
        help="This is the last exported time")
    hub_contact_last_updated = fields.Datetime(
        String="Hubspot Contacts Updated", readonly=True,
        help="Last Hubspot Contacts Updated Time")
    odoo_contact_last_updated = fields.Datetime(
        String="Odoo Contacts Updated", readonly=True,
        help="Last Odoo Contacts Updated Time")
    # Company last sync Time
    company_last_imported = fields.Datetime(
        string="Last Import Date", readonly=True,
        help="This is the last imported time")
    company_last_exported = fields.Datetime(
        string="Last Export Date", readonly=True,
        help="This is the last exported time")
    hub_company_last_updated = fields.Datetime(
        String="Hubspot Company Updated", readonly=True,
        help="Last Hubspot Company Updated Time")
    odoo_company_last_updated = fields.Datetime(
        String="Odoo Company Updated", readonly=True,
        help="Last Odoo Company Updated Time")
    # Deals last sync Time
    deals_last_imported = fields.Datetime(
        string="Last Import Date", readonly=True,
        help="This is the last imported time")
    deals_last_exported = fields.Datetime(
        string="Last Export Date", readonly=True,
        help="This is the last exported time")
    hub_deal_last_updated = fields.Datetime(
        String="Hubspot Deal Updated", readonly=True,
        help="Last Hubspot Deal Updated Time")
    odoo_deal_last_updated = fields.Datetime(
        String="Odoo Deal Updated", readonly=True,
        help="Last Odoo Deal Updated Time")
    ##################################################
    last_invoice_import_date = fields.Datetime(
        string="Last Import Date", readonly=True,
        help="This is the last imported time")
    last_invoice_export_date = fields.Datetime(
        string="Last Export Date", readonly=True,
        help="This is the last exported time")

    ###################################################

    def action_connect(self):
        if self.connection == False:
            owners_endpoint = 'https://api.hubapi.com/owners/v2/owners'
            headers = {'Authorization': f'Bearer {self.access_key}'}
            try:
                response = requests.get(owners_endpoint, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if str(data[0]['ownerId']) == self.owner_id:
                        self.connection = True
                        raise AccessError(_("Authenticated and Connected your HubSpot Account Successfully"))
                else:
                    print(
                        f"Failed to fetch owner details. Status code: {response.status_code}")
                    raise AccessError(_("Error when Fetching account info"))
            except requests.exceptions.RequestException as e:
                print(f"Error occurred: {e}")
                return None
        else:
            self.connection = False

    def action_contact_sync(self):
        """
        Method used to sync contacts it calls other methods related to
        contacts when user need specific condition on sync contacts
        """
        rainbow_msg = "Congrats, "
        if self.export_contacts:
            exported_count = self.action_export_partner()
            if exported_count > 0:
                rainbow_msg += f"# {exported_count} Contacts Exported"
        if self.import_contacts:
            imported_count = self.action_import_partner()
            if imported_count > 0:
                rainbow_msg += f", # {imported_count} Contacts Imported"
        if self.update_hub_contacts:
            hub_update_count = self.action_update_hub_partner()
            if hub_update_count > 0:
                rainbow_msg += f", # {hub_update_count} Hubspot Contacts Updated"
        if self.update_odoo_contacts:
            odoo_update_count = self.action_update_odoo_partner()
            if odoo_update_count > 0:
                rainbow_msg += f", # {odoo_update_count} Odoo Contacts Updated"
        # If there is no sync option modifies data
        if rainbow_msg == "Congrats, ":
            rainbow_msg += "Contacts are already synced"
        # Rainbow man displays status of sync
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_msg,
                'type': 'rainbow_man'
            }
        }

    def action_company_sync(self):
        rainbow_msg = "Congrats, "
        if self.export_company:
            exported_count = self.action_export_company()
            if exported_count > 0:
                rainbow_msg += f"# {exported_count} Companies Exported"
        if self.import_company:
            imported_count = self.action_import_company()
            if imported_count > 0:
                rainbow_msg += f", # {imported_count} Companies Imported"
        if self.update_hub_company:
            hub_update_count = self.action_update_hub_company()
            if hub_update_count > 0:
                rainbow_msg += f", # {hub_update_count} Hubspot Companies Updated"
        if self.update_odoo_company:
            odoo_update_count = self.action_update_odoo_company()
            if odoo_update_count > 0:
                rainbow_msg += f", # {odoo_update_count} Odoo Companies Updated"
        if rainbow_msg == "Congrats, ":
            rainbow_msg += "Companies are already synced"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_msg,
                'type': 'rainbow_man'
            }
        }

    def action_deal_sync(self):
        rainbow_msg = "Congrats, "
        if self.export_deals:
            exported_count = self.action_export_deals()
            if exported_count > 0:
                rainbow_msg += f"# {exported_count} Deals Exported"
        if self.import_deals:
            imported_count = self.action_import_deals()
            if imported_count > 0:
                rainbow_msg += f", # {imported_count} Deals Imported"
        if self.update_hub_deals:
            hub_update_count = self.action_update_hub_deals()
            if hub_update_count > 0:
                rainbow_msg += f", # {hub_update_count} Hubspot Deals Updated"
        if self.update_odoo_deals:
            odoo_update_count = self.action_update_odoo_deals()
            if odoo_update_count > 0:
                rainbow_msg += f", # {odoo_update_count} Odoo Deals Updated"
        if rainbow_msg == "Congrats, ":
            rainbow_msg += "Deals are already synced"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_msg,
                'type': 'rainbow_man'
            }
        }

    ##############################################################################################

    ##############################################################################################
    def action_export_partner(self):
        """
        Method used to Export Contacts from Odoo to Hubspot
        """
        # Set up HubSpot API connection
        api_key = self.access_key
        base_url = 'https://api.hubapi.com'
        # Lists fields and their properties need to add in hubspot
        partner_fields = [
            {
                'name': 'odoo_mail',
                'label': 'Mail',
                'type': 'string'
            },
            {
                'name': 'odoo_image_string',
                'label': 'Image String',
                'type': 'string'
            },
        ]
        for field in partner_fields:
            # Check each field in partner_fields exists in HubSpot or not
            endpoint = f"/properties/v1/contacts/properties/named/" \
                       f"{field['name']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            response = requests.get(base_url + endpoint, headers=headers)
            # Response returns a status code "200" when field exist in hubspot
            if response.status_code != 200:
                # Create custom field in HubSpot
                endpoint = '/properties/v1/contacts/properties'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {}'.format(api_key)
                }
                # Properties of Field ie, going to create
                payload = {
                    'name': field['name'],
                    'label': field['label'],
                    'description': 'Custom field created form odoo',
                    'groupName': 'contactinformation',
                    'type': field['type']
                }
                # API call for Field creation
                response = requests.post(base_url + endpoint, json=payload,
                                         headers=headers)
                # Returns status code "200" when successfully created the field
                if response.status_code == 200:
                    print(f"Custom field {field['name']} created successfully.")
                else:
                    print(
                        f"Failed to create custom field, Status code:"
                        f" {field['name']}.",
                        response.status_code)
                    # popup shows failed msg
        # Setting api client connection via api
        api_client = HubSpot(access_token=self.access_key)
        odoo_partners = self.env['res.partner'].search([])
        success_count = 0
        # Fetch HubSpot contact's ID as list
        hubspot_partners = [rec.properties['hs_object_id']
                            for rec in api_client.crm.contacts.get_all()]
        for rec in odoo_partners:
            # If the Odoo contact not present in Hubspot ID list export it
            if rec.hs_object_id not in hubspot_partners:
                properties = {
                    "firstname": rec.name,
                    "lastname": "",
                    "phone": rec.phone,
                    "website": rec.website,
                    "odoo_mail": rec.email,
                    "odoo_image_string": base64.b64encode(rec.image_1920).
                    decode('utf-8') if (rec.image_1920 and len(base64.b64encode(
                        rec.image_1920).decode('utf-8')) < 65500) else None
                }
                api_response = api_client.crm.contacts.basic_api.create(
                    simple_public_object_input_for_create=
                    SimplePublicObjectInput(properties))
                # If Exported then update Hubspot ID in Odoo
                if api_response:
                    rec.write({
                        'hs_object_id': api_response.properties['hs_object_id'],
                        'sync_mode': 'export'})
                else:
                    print("Not exported", api_response.status_code)
                success_count += 1
        # If Any record exported Create Sync History
        if success_count > 0:
            self.env['hubspot.sync.history'].sudo().create({
                'date': datetime.now(),
                'res_model_id': self.env.ref('base.model_res_partner').id,
                'sync_mode': 'export',
                'state': 'success',
                'count': success_count,
            })
        self.contacts_last_exported = datetime.now()
        # Returns Exported Count
        return success_count

    def action_import_partner(self):
        """Import contacts from Hubspot"""
        needed_fields = [
            "firstname", "lastname", "email", "odoo_mail", "hs_object_id",
            "odoo_image_string"
        ]
        api_client = HubSpot(access_token=self.access_key)
        odoo_partners = self.env['res.partner'].search([]).mapped(
            'hs_object_id')
        hubspot_partners = api_client.crm.contacts.get_all(
            properties=needed_fields)
        print(hubspot_partners)
        partners_to_create = []
        success_count = 0
        for rec in hubspot_partners:
            if rec.properties['hs_object_id'] not in odoo_partners:
                print(rec)
                partners_to_create.append({
                    'name': rec.properties['firstname'] + '' + rec.properties[
                        'lastname'] if rec.properties[
                        'lastname'] else rec.properties['firstname'],
                    'email': rec.properties['email'] if rec.properties[
                        'email'] else rec.properties[
                        'odoo_mail'] if rec.properties['odoo_mail'] else None,
                    'image_1920': base64.b64decode(
                        rec.properties['odoo_image_string']) if rec.properties[
                        'odoo_image_string'] else None,
                    'hs_object_id': rec.properties['hs_object_id'],
                    'sync_mode': 'import'
                })
                success_count += 1
        if partners_to_create:
            self.env['res.partner'].sudo().create(partners_to_create)
        if success_count > 0:
            self.env['hubspot.sync.history'].sudo().create({
                'date': datetime.now(),
                'res_model_id': self.env.ref('base.model_res_partner').id,
                'sync_mode': 'import',
                'state': 'success',
                'count': success_count,
            })
        self.contacts_last_imported = datetime.now()
        return success_count

    def action_update_hub_partner(self):
        print("update hub button")
        api_client = HubSpot(access_token=self.access_key)
        odoo_partners = self.env['res.partner'].search([])
        odoo_partners_list = odoo_partners.mapped('hs_object_id')
        hubspot_partners = api_client.crm.contacts.get_all()
        update_success = 0
        data_to_update = []
        for rec in hubspot_partners:
            if rec.properties['hs_object_id'] in odoo_partners_list:
                odoo_record = self.env['res.partner'].search(
                    [('hs_object_id', '=', rec.properties['hs_object_id'])])
                if odoo_record.write_date > (
                        self.hub_contact_last_updated or rec.updated_at.astimezone(
                    timezone.utc).replace(tzinfo=None)):
                    data_to_update.append({
                        'id': rec.properties['hs_object_id'],
                        'properties': {
                            "odoo_mail": odoo_record.email,
                            "firstname": odoo_record.name,
                            "lastname": "",
                            "phone": odoo_record.phone,
                            "website": odoo_record.website,
                            "odoo_image_string": base64.b64encode(
                                odoo_record.image_1920).decode('utf-8') if (
                                    odoo_record.image_1920 and len(base64.b64encode(
                                    odoo_record.image_1920).decode(
                                'utf-8')) < 65500) else ""
                        }
                    })
                    update_success += 1
        print("data_to_update: ", data_to_update)
        api_response = api_client.crm.contacts.batch_api.update(
            batch_input_simple_public_object_batch_input=
            BatchInputSimplePublicObjectBatchInput(data_to_update))
        if update_success > 0:
            self.hub_contact_last_updated = datetime.now()
            self.env['hubspot.sync.history'].sudo().create({
                'date': self.hub_contact_last_updated,
                'res_model_id': self.env.ref('base.model_res_partner').id,
                'sync_mode': 'hub_updated',
                'state': 'success',
                'count': update_success,
            })
            self.hub_contact_last_updated = datetime.now()
        return update_success

    def action_update_odoo_partner(self):
        print("update odoo button")
        api_client = HubSpot(access_token=self.access_key)
        odoo_partners = self.env['res.partner'].search([])
        odoo_partners_list = odoo_partners.mapped('hs_object_id')
        needed_fields = [
            "firstname", "lastname", "email", "odoo_mail", "hs_object_id",
            "odoo_image_string"
        ]
        hubspot_partners = api_client.crm.contacts.get_all(
            properties=needed_fields)
        hubspot_partners_list = [rec.properties['hs_object_id']
                                 for rec in hubspot_partners]
        update_success = 0
        data_to_update = []
        for rec in odoo_partners:
            if rec.hs_object_id in hubspot_partners_list:
                hubspot_partner = {h.id: h for h in hubspot_partners}
                hub_record = hubspot_partner.get(rec.hs_object_id, None)
                if hub_record.updated_at.astimezone(timezone.utc).replace(
                        tzinfo=None) > (
                        self.odoo_contact_last_updated or rec.write_date):
                    data_to_update = {
                        'name': hub_record.properties[
                                    'firstname'] + '' + hub_record.properties[
                                    'lastname'] if hub_record.properties[
                            'lastname'] else hub_record.properties['firstname'],
                        'email': hub_record.properties[
                            'email'] if hub_record.properties[
                            'email'] else hub_record.properties[
                            'odoo_mail'] if hub_record.properties[
                            'odoo_mail'] else None,
                        'image_1920': base64.b64decode(hub_record.properties[
                                'odoo_image_string']) if hub_record.properties[
                            'odoo_image_string'] else None,
                    }
                    update_success += 1
                    self.env['res.partner'].browse(rec.id).write(data_to_update)
        if update_success > 0:
            self.odoo_contact_last_updated = datetime.now()
            self.env['hubspot.sync.history'].sudo().create({
                'date': self.odoo_contact_last_updated,
                'res_model_id': self.env.ref('base.model_res_partner').id,
                'sync_mode': 'odoo_updated',
                'state': 'success',
                'count': update_success,
            })
            rainbow_message = f" Congrats, {update_success} " \
                              f"Contacts Updated Successfully "
        else:
            rainbow_message = "Congrats, Your Odoo Contacts Already Uptodate"
            self.odoo_contact_last_updated = datetime.now()
        return update_success

    ###################################################################################

    ###################################################################################
    def action_import_company(self):
        """Import company"""
        api_client = HubSpot(access_token=self.access_key)
        odoo_companies = self.env['res.company'].search([]).mapped(
            'hs_object_id')
        hubspot_companies = api_client.crm.companies.get_all()
        companies_to_create = []
        success_count = 0
        for rec in hubspot_companies:
            if rec.properties['hs_object_id'] not in odoo_companies:
                companies_to_create.append({
                    'name': rec.properties['name'],
                    'website': rec.properties['domain'],
                    'city': rec.properties['city'],
                    'phone': rec.properties['phone'],
                    'hs_object_id': rec.properties['hs_object_id'],
                    'sync_mode': 'import',
                })
                success_count += 1
        if companies_to_create:
            self.env['res.company'].sudo().create(companies_to_create)
        if success_count > 0:
            self.env['hubspot.sync.history'].sudo().create({
                'date': datetime.now(),
                'res_model_id': self.env.ref('base.model_res_company').id,
                'sync_mode': 'import',
                'state': 'success',
                'count': success_count,
            })
            rainbow_message = f" Congrats, {success_count} Companies Imported Successfully "
        else:
            rainbow_message = "Congrats, Your Odoo Companies Already Uptodate"
        self.deals_last_imported = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_message,
                'type': 'rainbow_man'
            }
        }

    def action_export_company(self):
        # Export company
        api_client = HubSpot(access_token=self.access_key)
        odoo_companies = self.env['res.company'].search([])
        hubspot_companies = []
        success_count = 0
        for rec in api_client.crm.companies.get_all():
            hubspot_companies.append(rec.properties['hs_object_id'])
        for rec in odoo_companies:
            if rec.hs_object_id not in hubspot_companies:
                properties = {
                    "city": rec.city,
                    "domain": rec.website,
                    "industry": "",
                    "name": rec.name,
                    "phone": rec.phone,
                }
                api_response = api_client.crm.companies.basic_api.create(
                    simple_public_object_input_for_create=SimplePublicObjectInput(
                        properties)
                )
                if api_response:
                    rec.write({
                        'hs_object_id': api_response.properties['hs_object_id'],
                        'sync_mode': 'export'
                    })
                success_count += 1
        if success_count > 0:
            self.env['hubspot.sync.history'].sudo().create({
                'date': datetime.now(),
                'res_model_id': self.env.ref('base.model_res_company').id,
                'sync_mode': 'export',
                'state': 'success',
                'count': success_count,
            })
            rainbow_message = f" Congrats, {success_count} Companies Exported Successfully "
        else:
            rainbow_message = "Congrats, Your Hubspot Companies Already Uptodate"
        self.company_last_exported = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_message,
                'type': 'rainbow_man'
            }
        }

    def action_update_odoo_company(self):
        print("update odoo company")
        api_client = HubSpot(access_token=self.access_key)
        odoo_company = self.env['res.company'].search([])
        needed_fields = ["name", "domain", "city", "phone", "hs_object_id"]
        hubspot_company = api_client.crm.companies.get_all(
            properties=needed_fields)
        hubspot_company_list = [rec.properties['hs_object_id']
                                for rec in hubspot_company]
        update_success = 0
        data_to_update = []
        for rec in odoo_company:
            if rec.hs_object_id in hubspot_company_list:
                hubspot_company_dict = {h.id: h for h in hubspot_company}
                hub_record = hubspot_company_dict.get(rec.hs_object_id, None)
                if hub_record.updated_at.astimezone(timezone.utc).replace(
                        tzinfo=None) > rec.write_date:
                    data_to_update = {
                        'name': hub_record.properties['name'],
                        'website': hub_record.properties['domain'],
                        'city': hub_record.properties['city'],
                        'phone': hub_record.properties['phone'],
                        'hs_object_id': hub_record.properties['hs_object_id'],
                    }
                    update_success += 1
                    self.env['res.company'].browse(rec.id).write(data_to_update)
        if update_success > 0:
            self.odoo_company_last_updated = datetime.now()
            self.env['hubspot.sync.history'].sudo().create({
                'date': self.odoo_company_last_updated,
                'res_model_id': self.env.ref('base.model_res_company').id,
                'sync_mode': 'odoo_updated',
                'state': 'success',
                'count': update_success,
            })
            rainbow_message = f" Congrats, {update_success} " \
                              f"Companies Updated Successfully "
        else:
            rainbow_message = "Congrats, Your Odoo Companies Already Uptodate"
            self.odoo_company_last_updated = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_message,
                'type': 'rainbow_man'
            }
        }

    def action_update_hub_company(self):
        print("update hub company")
        api_client = HubSpot(access_token=self.access_key)
        odoo_company = self.env['res.company'].search([])
        odoo_company_list = odoo_company.mapped('hs_object_id')
        hubspot_company = api_client.crm.companies.get_all()
        update_success = 0
        data_to_update = []
        for rec in hubspot_company:
            if rec.properties['hs_object_id'] in odoo_company_list:
                odoo_record = self.env['res.company'].search(
                    [('hs_object_id', '=', rec.properties['hs_object_id'])])
                if odoo_record.write_date > (
                        self.hub_company_last_updated or rec.updated_at.astimezone(
                    timezone.utc).replace(tzinfo=None)):
                    data_to_update.append({
                        'id': rec.properties['hs_object_id'],
                        'properties': {
                            "city": odoo_record.city,
                            "domain": odoo_record.website,
                            "industry": "",
                            "name": odoo_record.name,
                            "phone": odoo_record.phone,
                        }
                    })
                    update_success += 1
        api_response = api_client.crm.companies.batch_api.update(
            batch_input_simple_public_object_batch_input=BatchInputSimplePublicObjectBatchInput(
                data_to_update)
        )
        if update_success > 0:
            print(data_to_update)
            self.hub_company_last_updated = datetime.now()
            self.env['hubspot.sync.history'].sudo().create({
                'date': self.hub_company_last_updated,
                'res_model_id': self.env.ref('base.model_res_company').id,
                'sync_mode': 'hub_updated',
                'state': 'success',
                'count': update_success,
            })
            rainbow_message = f" Congrats, {update_success} " \
                              f"Company Updated Successfully "
        else:
            rainbow_message = "Congrats, Your Odoo Company Already Uptodate"
            self.hub_company_last_updated = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_message,
                'type': 'rainbow_man'
            }
        }

    ########################################################################################

    ###################################################################################
    def action_import_deals(self):
        """Import Deals"""
        needed_fields = [
            "amount", "closedate", "dealname", "hubspot_owner_id",
            "pipeline", "odoo_type", "odoo_probability", "odoo_stage_id",
            "odoo_partner_id", "odoo_team_id", "odoo_contact_name",
            "odoo_email_from", "odoo_phone"
        ]
        api_client = HubSpot(access_token=self.access_key)
        odoo_deals = self.env['crm.lead'].search([]).mapped('hs_object_id')
        hubspot_deals = api_client.crm.deals.get_all(properties=needed_fields)
        # hubspot_deals = api_client.crm.deals.get_all(
        #     properties={'properties': needed_fields})
        # print(hubspot_deals)
        deals_to_create = []
        hs_stages = {
            stage.hs_stage: stage.id for stage in self.env['crm.stage'].search(
                [('hs_stage', '!=', False)])}
        success_count = 0
        for rec in hubspot_deals:
            if rec.properties['hs_object_id'] not in odoo_deals:
                deals_to_create.append({
                    'name': rec.properties['dealname'] or 'Lead',
                    'hs_object_id': rec.properties['hs_object_id'],
                    'expected_revenue': rec.properties['amount'],
                    'stage_id': rec.properties['odoo_stage_id'],
                    'date_deadline': rec.properties['closedate'],
                    'type': rec.properties['odoo_type'],
                    'probability': rec.properties['odoo_probability'],
                    # 'partner_id': rec.properties['odoo_partner_id'] if rec.properties['odoo_partner_id'] else 0,
                    # 'team_id': rec.properties['odoo_team_id'] if rec.properties['odoo_team_id'] else 0,
                    'contact_name': rec.properties['odoo_contact_name'],
                    'email_from': rec.properties['odoo_email_from'],
                    'phone': rec.properties['odoo_phone'],
                    'sync_mode': 'import',
                })
                success_count += 1
        if deals_to_create:
            self.env['crm.lead'].sudo().create(deals_to_create)
        if success_count > 0:
            self.env['hubspot.sync.history'].sudo().create({
                'date': datetime.now(),
                'res_model_id': self.env.ref('crm.model_crm_lead').id,
                'sync_mode': 'import',
                'state': 'success',
                'count': success_count,
            })
            rainbow_message = f" Congrats, {success_count} Deals Imported Successfully "
        else:
            rainbow_message = "Congrats, Your Odoo Deals Already Uptodate"
        self.deals_last_imported = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_message,
                'type': 'rainbow_man'
            }
        }

    def action_export_deals(self):
        """Export Deals"""
        # Set up HubSpot API connection
        api_key = self.access_key
        base_url = 'https://api.hubapi.com'
        # Field name to check
        deal_fields = [
            {
                'name': 'odoo_type',
                'label': 'Type',
                'type': 'string'
            },
            {
                'name': 'odoo_probability',
                'label': 'Probability',
                'type': 'number'
            },
            {
                'name': 'odoo_stage_id',
                'label': 'Stage ID',
                'type': 'number'
            },
            {
                'name': 'odoo_partner_id',
                'label': 'User ID',
                'type': 'number'
            },
            {
                'name': 'odoo_team_id',
                'label': 'Team ID',
                'type': 'number'
            },
            {
                'name': 'odoo_contact_name',
                'label': 'Contact Name',
                'type': 'string'
            },
            {
                'name': 'odoo_email_from',
                'label': 'Email',
                'type': 'string'
            },
            {
                'name': 'odoo_phone',
                'label': 'Phone',
                'type': 'string'
            }
        ]
        for field in deal_fields:
            # Check if 'type' field exists in HubSpot
            endpoint = f"/properties/v1/deals/properties/named/{field['name']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            response = requests.get(base_url + endpoint, headers=headers)
            if response.status_code != 200:
                print(
                    f"The field {field['name']} does not exists in deals in HubSpot.")
                # Create custom field in HubSpot
                endpoint = '/properties/v1/deals/properties'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {}'.format(api_key)
                }
                payload = {
                    'name': field['name'],
                    'label': field['label'],
                    'description': 'Custom field created programmatically',
                    'groupName': 'dealinformation',
                    'type': field['type']
                }
                print(payload)
                response = requests.post(base_url + endpoint, json=payload,
                                         headers=headers)
                if response.status_code == 200:
                    print(f"Custom field {field['name']} created successfully.")
                else:
                    print(
                        f"Failed to create custom field {field['name']}. Status code:",
                        response.status_code)
                    # popup shows failed msg
            else:
                print(f"The field {field['name']} exist in deals in HubSpot.")
        # Export include newly created fields
        api_client = HubSpot(access_token=self.access_key)
        odoo_deals = self.env['crm.lead'].search([])
        hubspot_deals = []
        success_count = 0
        for rec in api_client.crm.deals.get_all():
            hubspot_deals.append(rec.properties['hs_object_id'])
        for rec in odoo_deals:
            if rec.hs_object_id not in hubspot_deals:
                properties = {
                    "amount": rec.expected_revenue if rec.expected_revenue else None,
                    "closedate": rec.date_deadline if rec.date_deadline else '',
                    "dealname": rec.name,
                    "hubspot_owner_id": self.owner_id,
                    "pipeline": "default",
                    "odoo_type": rec.type,
                    "odoo_probability": rec.probability if rec.probability else None,
                    "odoo_stage_id": rec.stage_id.id if rec.stage_id else None,
                    "odoo_partner_id": rec.partner_id.id if rec.partner_id else None,
                    "odoo_team_id": rec.team_id.id if rec.team_id else None,
                    "odoo_contact_name": rec.contact_name if rec.contact_name else None,
                    "odoo_email_from": rec.email_from if rec.email_from else None,
                    "odoo_phone": rec.phone if rec.phone else None
                }
                print(properties)
                api_response = api_client.crm.deals.basic_api.create(
                    simple_public_object_input_for_create=SimplePublicObjectInput(
                        properties)
                )
                if api_response:
                    rec.write({
                        'hs_object_id': api_response.properties['hs_object_id'],
                        'sync_mode': 'export'
                    })
                success_count += 1
        if success_count > 0:
            self.env['hubspot.sync.history'].sudo().create({
                'date': datetime.now(),
                'res_model_id': self.env.ref('crm.model_crm_lead').id,
                'sync_mode': 'export',
                'state': 'success',
                'count': success_count,
            })
            rainbow_message = f" Congrats, {success_count} Deals Exported Successfully "
        else:
            rainbow_message = "Congrats, Your Hubspot Deals Already Uptodate"
        self.deals_last_exported = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_message,
                'type': 'rainbow_man'
            }
        }

    def action_update_odoo_deals(self):
        print("update odoo deals")
        api_client = HubSpot(access_token=self.access_key)
        odoo_deal = self.env['crm.lead'].search([])
        needed_fields = [
            "dealname", "hs_object_id", "amount", "odoo_stage_id", "closedate",
            "odoo_type", "odoo_probability", "odoo_contact_name",
            "odoo_email_from", "odoo_phone"
        ]
        hubspot_deal = api_client.crm.deals.get_all(
            properties=needed_fields)
        hubspot_deal_list = [rec.properties['hs_object_id']
                             for rec in hubspot_deal]
        update_success = 0
        data_to_update = []
        for rec in odoo_deal:
            if rec.hs_object_id in hubspot_deal_list:
                hubspot_deal_dict = {h.id: h for h in hubspot_deal}
                hub_record = hubspot_deal_dict.get(rec.hs_object_id, None)
                if hub_record.updated_at.astimezone(timezone.utc).replace(
                        tzinfo=None) > rec.write_date:
                    data_to_update = {
                        'name': hub_record.properties['dealname'] or 'Lead',
                        'expected_revenue': hub_record.properties['amount'],
                        'stage_id': int(hub_record.properties['odoo_stage_id']),
                        'date_deadline': hub_record.properties['closedate'],
                        'type': hub_record.properties['odoo_type'],
                        'probability': float(
                            hub_record.properties['odoo_probability']),
                        # 'partner_id': hub_record.properties['odoo_partner_id'] if hub_record.properties['odoo_partner_id'] else 0,
                        # 'team_id': hub_record.properties['odoo_team_id'] if hub_record.properties['odoo_team_id'] else 0,
                        'contact_name': hub_record.properties[
                            'odoo_contact_name'],
                        'email_from': hub_record.properties['odoo_email_from'],
                        'phone': hub_record.properties['odoo_phone'],
                    }
                    update_success += 1
                    self.env['crm.lead'].browse(rec.id).write(data_to_update)
        if update_success > 0:
            self.odoo_deal_last_updated = datetime.now()
            self.env['hubspot.sync.history'].sudo().create({
                'date': self.odoo_deal_last_updated,
                'res_model_id': self.env.ref('crm.model_crm_lead').id,
                'sync_mode': 'odoo_updated',
                'state': 'success',
                'count': update_success,
            })
            rainbow_message = f" Congrats, {update_success} " \
                              f"Leads Updated Successfully "
        else:
            rainbow_message = "Congrats, Your Odoo Leads Already Uptodate"
            self.odoo_deal_last_updated = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_message,
                'type': 'rainbow_man'
            }
        }

    def action_update_hub_deals(self):
        print("update hub dwals")
        api_client = HubSpot(access_token=self.access_key)
        odoo_deal = self.env['crm.lead'].search([])
        odoo_deal_list = odoo_deal.mapped('hs_object_id')
        hubspot_deal = api_client.crm.deals.get_all()
        update_success = 0
        data_to_update = []
        for rec in hubspot_deal:
            if rec.properties['hs_object_id'] in odoo_deal_list:
                odoo_record = self.env['crm.lead'].search(
                    [('hs_object_id', '=', rec.properties['hs_object_id'])])
                if odoo_record.write_date > rec.updated_at.astimezone(
                        timezone.utc).replace(tzinfo=None):
                    data_to_update.append({
                        'id': rec.properties['hs_object_id'],
                        'properties': {
                            "amount": odoo_record.expected_revenue if odoo_record.expected_revenue else None,
                            "closedate": odoo_record.date_deadline if odoo_record.date_deadline else '',
                            "dealname": odoo_record.name,
                            "hubspot_owner_id": self.owner_id,
                            "pipeline": "default",
                            "odoo_type": odoo_record.type,
                            "odoo_probability": odoo_record.probability if odoo_record.probability else None,
                            "odoo_stage_id": odoo_record.stage_id.id if odoo_record.stage_id else None,
                            "odoo_partner_id": odoo_record.partner_id.id if odoo_record.partner_id else None,
                            "odoo_team_id": odoo_record.team_id.id if odoo_record.team_id else None,
                            "odoo_contact_name": odoo_record.contact_name if odoo_record.contact_name else None,
                            "odoo_email_from": odoo_record.email_from if odoo_record.email_from else None,
                            "odoo_phone": odoo_record.phone if odoo_record.phone else None
                        }
                    })
                    update_success += 1
        api_response = api_client.crm.deals.batch_api.update(
            batch_input_simple_public_object_batch_input=BatchInputSimplePublicObjectBatchInput(
                data_to_update)
        )
        if update_success > 0:
            print(data_to_update)
            self.hub_deal_last_updated = datetime.now()
            self.env['hubspot.sync.history'].sudo().create({
                'date': self.hub_deal_last_updated,
                'res_model_id': self.env.ref('crm.model_crm_lead').id,
                'sync_mode': 'hub_updated',
                'state': 'success',
                'count': update_success,
            })
            rainbow_message = f" Congrats, {update_success} " \
                              f"Hub Deals Updated Successfully "
        else:
            rainbow_message = "Congrats, Your Hub Deals Already Uptodate"
            self.hub_company_last_updated = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': rainbow_message,
                'type': 'rainbow_man'
            }
        }

    #######################################################################################

    def action_import_invoice(self):
        print("import button ook")

    def action_export_invoice(self):
        print("export button ook")
