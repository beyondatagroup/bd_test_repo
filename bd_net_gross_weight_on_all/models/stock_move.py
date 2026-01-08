from odoo import models, fields,api,_
from datetime import date, timedelta

class StockPicking(models.Model):
    _inherit = "stock.picking"

    display_weight = fields.Boolean("Display weight report?")
    display_weight_subtotel = fields.Boolean("Display weight column Subtotal?")

    total_net_weight = fields.Float(
        string="Total Net Weight", compute="_compute_total_weights",store=True
    )
    total_gross_weight = fields.Float(
        string="Total Gross Weight", compute="_compute_total_weights",store=True
    )

    @api.depends('move_ids.total_net_weight', 'move_ids.total_gross_weight')
    def _compute_total_weights(self):
        for picking in self:
            picking.total_net_weight = sum(picking.move_ids.mapped('total_net_weight') or [])
            picking.total_gross_weight = sum(picking.move_ids.mapped('total_gross_weight') or [])

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



class StockMove(models.Model):
    _inherit = "stock.move"

    net_weight = fields.Float(string="Net Weight",related="product_id.net_weight",store=True)
    gross_weight = fields.Float(string="Gross Weight",related="product_id.gross_weight",store=True)
    total_net_weight = fields.Float(string="Total Net Weight", compute="_compute_total_weights", store=True)
    total_gross_weight = fields.Float(string="Total Gross Weight", compute="_compute_total_weights", store=True)

    @api.onchange('product_id')
    def _onchange_product_weight(self):
        for move in self:
            move.net_weight = move.product_id.net_weight or 0.0
            move.gross_weight = move.product_id.gross_weight or 0.0

    @api.depends('net_weight', 'gross_weight', 'product_uom_qty')
    def _compute_total_weights(self):
        for move in self:
            move.total_net_weight = (move.net_weight or 0.0) * (move.product_uom_qty or 0.0)
            move.total_gross_weight = (move.gross_weight or 0.0) * (move.product_uom_qty or 0.0)
