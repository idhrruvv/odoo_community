from odoo import models, fields

class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    commission = fields.Float(string="Commission (%)")


# from odoo import models, fields, api
# from odoo.exceptions import UserError


# class EstateProperty(models.Model):
#     _inherit = "estate.property"

#     commission_percentage = fields.Float(string="Commission (%)")

#     accepted_offer_price = fields.Float(
#         string="Accepted Offer Price",
#         readonly=True,
#         copy=False
#     )

#     commission_amount = fields.Float(
#         string="Commission Amount",
#         compute="_compute_commission",
#         store=True
#     )

#     final_amount = fields.Float(
#         string="Total Amount With Commission",
#         compute="_compute_commission",
#         store=True
#     )

#     @api.depends("commission_percentage", "accepted_offer_price")
#     def _compute_commission(self):
#         for record in self:
#             if record.accepted_offer_price and record.commission_percentage:
#                 record.commission_amount = (
#                     record.accepted_offer_price * record.commission_percentage / 100
#                 )
#                 record.final_amount = (
#                     record.accepted_offer_price + record.commission_amount
#                 )
#             else:
#                 record.commission_amount = 0.0
#                 record.final_amount = 0.0

#     # 🔥 OVERRIDE MARK AS SOLD
#     def action_accept(self):
#         for record in self:
#             if record.state != 'accept':
#                 raise UserError("Only Accepted offer can be marked as Sold.")

#             # get accepted offer
#             accepted_offer = self.env["estate.property.offer"].search([
#                 ("property_id", "=", record.id),
#                 ("status", "=", "accepted")
#             ], limit=1)

#             if not accepted_offer:
#                 raise UserError("No accepted offer found.")

#             record.accepted_offer_price = accepted_offer.price
#             record.selling_price = accepted_offer.price
#             record.state = "sold"

#             # Auto update description
#             record.description = f"""
# Accepted Offer Price : {record.accepted_offer_price}

# Commission ({record.commission_percentage}%):
# {record.commission_amount}

# Total Amount With Commission:
# {record.final_amount}
# """
