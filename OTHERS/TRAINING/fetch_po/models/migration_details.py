from odoo import fields, models


class MigrationDetails(models.Model):
    """ Model for storing Migration details """

    _name = "migration.details"
    _description = "Migration details"
    _inherit = 'mail.thread'
    _rec_name = 'data'

    data = fields.Char("Migrated data")
    database_from = fields.Char("Migration From")
    database_to = fields.Char("Migration To")
    count = fields.Integer("Migrated records")
    user = fields.Char("User")
    date = fields.Date("Date")
