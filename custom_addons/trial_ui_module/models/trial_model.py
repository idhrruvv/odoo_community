from odoo import models, fields

class TrialModel(models.Model):
    _name = 'trial.model'
    _description = 'Trial Model'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")