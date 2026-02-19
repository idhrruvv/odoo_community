from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reference_note = fields.Char(string="Reference Note")
