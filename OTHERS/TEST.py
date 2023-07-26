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

################################################################################
CONTACTS
FIELDS
################################################################################
name = fields.Char(index=True, default_export_compatible=True)
display_name = fields.Char(compute='_compute_display_name', recursive=True,
                           store=True, index=True)
date = fields.Date(index=True)
title = fields.Many2one('res.partner.title')
parent_id = fields.Many2one('res.partner', string='Related Company', index=True)
parent_name = fields.Char(related='parent_id.name', readonly=True,
                          string='Parent name')
child_ids = fields.One2many('res.partner', 'parent_id', string='Contact',
                            domain=[('active', '=',
                                     True)])  # force "active_test" domain to bypass _search() override
ref = fields.Char(string='Reference', index=True)
lang = fields.Selection(_lang_get, string='Language',
                        help="All the emails and documents sent to this contact will be translated in this language.")
active_lang_count = fields.Integer(compute='_compute_active_lang_count')
tz = fields.Selection(_tz_get, string='Timezone',
                      default=lambda self: self._context.get('tz'),
                      help="When printing documents and exporting/importing data, time values are computed according to this timezone.\n"
                           "If the timezone is not set, UTC (Coordinated Universal Time) is used.\n"
                           "Anywhere else, time values are computed according to the time offset of your web client.")

tz_offset = fields.Char(compute='_compute_tz_offset', string='Timezone offset',
                        invisible=True)
user_id = fields.Many2one(
    'res.users', string='Salesperson',
    compute='_compute_user_id',
    precompute=True,  # avoid queries post-create
    readonly=False, store=True,
    help='The internal user in charge of this contact.')
vat = fields.Char(string='Tax ID', index=True,
                  help="The Tax Identification Number. Values here will be validated based on the country format. You can use '/' to indicate that the partner is not subject to tax.")
same_vat_partner_id = fields.Many2one('res.partner',
                                      string='Partner with same Tax ID',
                                      compute='_compute_same_vat_partner_id',
                                      store=False)
same_company_registry_partner_id = fields.Many2one('res.partner',
                                                   string='Partner with same Company Registry',
                                                   compute='_compute_same_vat_partner_id',
                                                   store=False)
company_registry = fields.Char(string="Company ID",
                               compute='_compute_company_registry', store=True,
                               readonly=False,
                               help="The registry number of the company. Use it if it is different from the Tax ID. It must be unique across all partners of a same country")
bank_ids = fields.One2many('res.partner.bank', 'partner_id', string='Banks')
website = fields.Char('Website Link')
comment = fields.Html(string='Notes')

category_id = fields.Many2many('res.partner.category', column1='partner_id',
                               column2='category_id', string='Tags',
                               default=_default_category)
active = fields.Boolean(default=True)
employee = fields.Boolean(help="Check this box if this contact is an Employee.")
function = fields.Char(string='Job Position')
type = fields.Selection(
    [('contact', 'Contact'),
     ('invoice', 'Invoice Address'),
     ('delivery', 'Delivery Address'),
     ('private', 'Private Address'),
     ('other', 'Other Address'),
     ], string='Address Type',
    default='contact',
    help="- Contact: Use this to organize the contact details of employees of a given company (e.g. CEO, CFO, ...).\n"
         "- Invoice Address : Preferred address for all invoices. Selected by default when you invoice an order that belongs to this company.\n"
         "- Delivery Address : Preferred address for all deliveries. Selected by default when you deliver an order that belongs to this company.\n"
         "- Private: Private addresses are only visible by authorized users and contain sensitive data (employee home addresses, ...).\n"
         "- Other: Other address for the company (e.g. subsidiary, ...)")
# address fields
street = fields.Char()
street2 = fields.Char()
zip = fields.Char(change_default=True)
city = fields.Char()
state_id = fields.Many2one("res.country.state", string='State',
                           ondelete='restrict',
                           domain="[('country_id', '=?', country_id)]")
country_id = fields.Many2one('res.country', string='Country',
                             ondelete='restrict')
country_code = fields.Char(related='country_id.code', string="Country Code")
partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
email = fields.Char()
email_formatted = fields.Char(
    'Formatted Email', compute='_compute_email_formatted',
    help='Format email address "Name <email@domain>"')
phone = fields.Char(unaccent=False)
mobile = fields.Char(unaccent=False)
is_company = fields.Boolean(string='Is a Company', default=False,
                            help="Check if the contact is a company, otherwise it is a person")
is_public = fields.Boolean(compute='_compute_is_public')
industry_id = fields.Many2one('res.partner.industry', 'Industry')
# company_type is only an interface field, do not use it in business logic
company_type = fields.Selection(string='Company Type',
                                selection=[('person', 'Individual'),
                                           ('company', 'Company')],
                                compute='_compute_company_type',
                                inverse='_write_company_type')
company_id = fields.Many2one('res.company', 'Company', index=True)
color = fields.Integer(string='Color Index', default=0)
user_ids = fields.One2many('res.users', 'partner_id', string='Users',
                           auto_join=True)
partner_share = fields.Boolean(
    'Share Partner', compute='_compute_partner_share', store=True,
    help="Either customer (not a user), either shared user. Indicated the current partner is a customer without "
         "access or with a limited access created for sharing data.")
contact_address = fields.Char(compute='_compute_contact_address',
                              string='Complete Address')

# technical field used for managing commercial fields
commercial_partner_id = fields.Many2one(
    'res.partner', string='Commercial Entity',
    compute='_compute_commercial_partner', store=True,
    recursive=True, index=True)
commercial_company_name = fields.Char('Company Name Entity',
                                      compute='_compute_commercial_company_name',
                                      store=True)
company_name = fields.Char('Company Name')
barcode = fields.Char(help="Use a barcode to identify this contact.",
                      copy=False, company_dependent=True)
