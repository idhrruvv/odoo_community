from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(required=True)
    description = fields.Text() 
    offers = fields.One2many(
    'estate.property.offer',
    'property_id',
    string="Offers"
)
    
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    buyer_id = fields.Many2one('res.partner', string='Buyer', readonly=True)

    seller_id = fields.Many2one('res.partner', string='Seller', required=True)

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer()
    living_area = fields.Float()
    garden_area = fields.Float()
    total_area = fields.Float(compute='_compute_total_area', store=True)

    facades = fields.Integer()
    garden = fields.Boolean()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])

    postcode = fields.Char()
    date_available = fields.Date(default=fields.Date.today,required=True)
    # @api.constrains('date_available')
    # def _check_date_available(self):
    #     for rec in self:
    #         if rec.date_available and rec.date_available <= Date.today():
    #             raise Exception("Available date cannot be in the past!")


    state = fields.Selection([
        ('new', 'New'),
        ('accept','Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], default='new',tracking=True)


    # def _group_expand_states(self):
    #     return ['new', 'accept', 'sold', 'cancelled']

    def action_sold(self):
        for record in self:
            if record.state != 'new':
                raise UserError("Only New properties can be sold.")
            record.state = 'sold'      
        
    def action_accept(self):
        for record in self:
            if record.state != 'accept':
                raise UserError("Accepted can not be cancelled")
            record.state = "sold"

    # def action_accept(self):
    #     for rec in self:
    #         if rec.state != 'accept':
    #             raise UserError("Only accepted property can be marked as Sold.")

    #         accepted_offer = rec.offers.filtered(
    #             lambda o: o.status == 'accepted'
    #         )

    #         if not accepted_offer:
    #             raise UserError("No accepted offer found!")

    #         offer = accepted_offer[0]

    #         rec.accepted_offer_price = offer.price
    #         rec.selling_price = offer.price
    #         rec.state = 'sold'


    def action_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be cancelled.")
            record.state = 'cancelled'

    tag_ids = fields.Many2many('estate.property.tag', string="Tags")

    active = fields.Boolean(default=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = (rec.living_area or 0.0) + (rec.garden_area or 0.0)

    # SMART OFFER BUTTONS

    offer_count = fields.Integer(
        compute="_compute_offer_count",
        string="Offer Count"
    )

    @api.depends("offers")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offers)

    def action_view_offers(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": {
                "default_property_id": self.id,
            },
        }


# COMMISSION CALCULATION
    commission_percentage = fields.Float(string="Commission (%)")

    accepted_offer_price = fields.Float(
        string="Accepted Offer Price",
        readonly=True,
        copy=False
    )

    commission_amount = fields.Float(
        string="Commission Amount",
        compute="_compute_commission",
        store=True
    )

    final_amount = fields.Float(
        string="Total Amount With Commission",
        compute="_compute_commission",
        store=True
    )

    @api.depends("commission_percentage", "accepted_offer_price")
    def _compute_commission(self):
        for rec in self:
            if rec.accepted_offer_price:
                rec.commission_amount = (
                    rec.accepted_offer_price * rec.commission_percentage / 100
                )
                rec.final_amount = (
                    rec.accepted_offer_price + rec.commission_amount
                )
            else:
                rec.commission_amount = 0.0
                rec.final_amount = 0.0


