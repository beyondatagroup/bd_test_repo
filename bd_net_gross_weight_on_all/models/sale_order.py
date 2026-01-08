from odoo import models, fields,api,_
from datetime import date, timedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"

    display_weight = fields.Boolean("Display weight report?")
    display_weight_subtotel = fields.Boolean("Display weight column Subtotal?")

    def action_black_net(self):
        """Your custom server action function"""
        for rec in self:
            # Example action
            rec.display_weight = True
            # rec.display_weight_subtotel = True
        return True

    def action_black_gross(self):
        """Your custom server action function"""
        for rec in self:
            # Example action
            # rec.display_weight = True
            rec.display_weight_subtotel = True
        return True

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    net_weight = fields.Float(string="Net Weight",related="product_id.net_weight",store=True)
    gross_weight = fields.Float(string="Gross Weight",related="product_id.gross_weight",store=True)
    total_net_weight = fields.Float(string="Total Net Weight", compute="_compute_total_weights", store=True)
    total_gross_weight = fields.Float(string="Total Gross Weight", compute="_compute_total_weights", store=True)

    @api.onchange('product_id')
    def _onchange_product_weight(self):
        for line in self:
            line.net_weight = line.product_id.net_weight or 0.0
            line.gross_weight = line.product_id.gross_weight or 0.0

    @api.depends('net_weight', 'gross_weight', 'product_uom_qty')
    def _compute_total_weights(self):
        for line in self:
            line.total_net_weight = (line.net_weight or 0.0) * (line.product_uom_qty or 0.0)
            line.total_gross_weight = (line.gross_weight or 0.0) * (line.product_uom_qty or 0.0)