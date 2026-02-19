from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # pehle property ko sold mark karo
        super().action_sold()

        for rec in self:
            # Buyer invoice create karo
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': rec.buyer_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': "Property Sold",
                        'quantity': 1,
                        'price_unit': rec.selling_price,
                    }),
                ],
            }
            self.env['account.move'].create(invoice_vals)
