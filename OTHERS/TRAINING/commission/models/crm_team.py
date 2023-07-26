from odoo import fields, models, api


class CrmTeam(models.Model):
    """ model for adding commission plan field in crm_team page """
    # _name = "crm.team"
    _inherit = 'crm.team'

    commission_plan_id = fields.Many2one('commission.plan', 'Commission Plan')

    @api.onchange('commission_plan_id')
    def _onchange_commission_plan_id(self):
        """ assign plan for sales persons under this team which are currently not applied """
        for member in self.env['crm.team.member'].search([]):
            if not member.commission_plan_id:
                if member.crm_team_id and member.crm_team_id.commission_plan_id:
                    member.commission_plan_id = member.crm_team_id.commission_plan_id
                    print(member.commission_plan_id)
