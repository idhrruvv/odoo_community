from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = 'price desc'

    price = fields.Float(required=True)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True,ondelete="cascade")

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", copy=False)



    # ----------------------------------
    # VALIDATION → 90% Rule
    # ----------------------------------
    @api.constrains('price')
    def _check_offer_price(self):
        for rec in self:
            if rec.price < rec.property_id.expected_price * 0.9:
                raise ValidationError(
                    "Offer must be at least 90% of expected price!"
                )

    # ----------------------------------
    # ACCEPT BUTTON
    # ----------------------------------

    #only offer will be accepted but commission is not calculating

    # def action_accept(self):
    #     for rec in self:

    #         # Check if already accepted offer exists
    #         accepted_offer = rec.property_id.offers.filtered(
    #             lambda o: o.status == 'accepted'
    #         )

    #         if accepted_offer:
    #             raise ValidationError("Only one offer can be accepted!")

    #         # Update this offer
    #         rec.status = 'accepted'

    #         # Update property automatically
    #         rec.property_id.write({
    #             'selling_price': rec.price,
    #             'buyer_id': rec.partner_id.id,
    #             'state': 'accept'
    #         })

    #Commission calculation with offer accepted code 

    def action_accept(self):
        for rec in self:

            accepted_offer = rec.property_id.offers.filtered(
                lambda o: o.status == 'accepted'
            )

            if accepted_offer:
                raise ValidationError("Only one offer can be accepted!")

            # Mark offer accepted
            rec.status = 'accepted'

            # Update property
            rec.property_id.write({
                'accepted_offer_price': rec.price,
                'selling_price': rec.price,
                'buyer_id': rec.partner_id.id,
                'state': 'accept',  
            })


    # ----------------------------------
    # REFUSE BUTTON
    # ----------------------------------
    def action_refuse(self):
        for rec in self:
            if rec.status == 'accepted':
                raise ValidationError("Accepted offer cannot be refused!")
            rec.status = 'refused'


