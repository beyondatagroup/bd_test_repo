from odoo import models, fields,api,_
from datetime import date, timedelta

class AccountMove(models.Model):
    _inherit = "account.move"

    display_weight = fields.Boolean("Display weight report?")
    display_weight_subtotel = fields.Boolean("Display weight column Subtotal?")

    total_net_weight = fields.Float(
        string="Total Net Weight", compute="_compute_total_weights", store=True
    )
    total_gross_weight = fields.Float(
        string="Total Gross Weight", compute="_compute_total_weights", store=True
    )

    @api.depends('invoice_line_ids.net_weight', 'invoice_line_ids.gross_weight', 'invoice_line_ids.quantity')
    def _compute_total_weights(self):
        for move in self:
            total_net = 0.0
            total_gross = 0.0
            for line in move.invoice_line_ids:
                total_net += (line.net_weight or 0.0) * (line.quantity or 0.0)
                total_gross += (line.gross_weight or 0.0) * (line.quantity or 0.0)
            move.total_net_weight = total_net
            move.total_gross_weight = total_gross


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


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    net_weight = fields.Float(string="Net Weight",related="product_id.net_weight",store=True)
    gross_weight = fields.Float(string="Gross Weight",related="product_id.gross_weight",store=True)
    total_net_weight = fields.Float(string="Total Net Weight", compute="_compute_total_weights", store=True)
    total_gross_weight = fields.Float(string="Total Gross Weight", compute="_compute_total_weights", store=True)

    @api.onchange('product_id')
    def _onchange_product_weight(self):
        for line in self:
            line.net_weight = line.product_id.net_weight or 0.0
            line.gross_weight = line.product_id.gross_weight or 0.0

    @api.depends('net_weight', 'gross_weight', 'quantity')
    def _compute_total_weights(self):
        for line in self:
            line.total_net_weight = (line.net_weight or 0.0) * (line.quantity or 0.0)
            line.total_gross_weight = (line.gross_weight or 0.0) * (line.quantity or 0.0)