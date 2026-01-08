from odoo import models, fields,api,_
from datetime import date, timedelta
from odoo.fields import Command, Domain

class ResUsers(models.Model):
    _inherit = "res.users"

    sale_net_gross = fields.Boolean(
        string="Net and Gross Weight on Sale Order",
        compute="_compute_sale_net_gross",
        inverse="_inverse_sale_net_gross",
        store=True
    )
    purchase_net_gross = fields.Boolean(
        string="Net and Gross Weight on Purchase Order",
        compute="_compute_purchase_net_gross",
        inverse="_inverse_purchase_net_gross",
        store=True
    )
    transfers_net_gross = fields.Boolean(
        string="Net and Gross Weight on Delivery/Transfers",
        compute="_compute_transfers_net_gross",
        inverse="_inverse_transfers_net_gross",
        store=True
    )
    invoicing_net_gross = fields.Boolean(
        string="Net and Gross Weight on Invoicing Order",
        compute="_compute_invoicing_net_gross",
        inverse="_inverse_invoicing_net_gross",
        store=True
    )

    # Example for sale_net_gross
    def _compute_sale_net_gross(self):
        group = self.env.user.has_group("group_net_gross_weight_sale")
        for user in self:
            if group:
                user.sale_net_gross = group in user.groups_id

    def _inverse_sale_net_gross(self):
        group = [Command.link(self.env.ref('bd_net_gross_weight_on_all.group_net_gross_weight_sale').id)]
        for user in self:
            if user.sale_net_gross:
                self.env.user.sudo().group_ids = group
            else:
                self.env.user.sudo().group_ids = [(3, self.env.ref('bd_net_gross_weight_on_all.group_net_gross_weight_sale').id)]

    # Repeat similar compute/inverse for purchase_net_gross
    def _compute_purchase_net_gross(self):
        group = self.env.user.has_group("bd_net_gross_weight_on_all.group_net_gross_weight_purchase")
        for user in self:
            if group:
                user.purchase_net_gross = group in user.groups_id

    def _inverse_purchase_net_gross(self):
        group = [Command.link(self.env.ref('bd_net_gross_weight_on_all.group_net_gross_weight_purchase').id)]
        for user in self:
            if user.purchase_net_gross:
                self.env.user.sudo().group_ids = group
            else:
                self.env.user.sudo().group_ids = [(3, self.env.ref('bd_net_gross_weight_on_all.group_net_gross_weight_purchase').id)]

    # Repeat for transfers_net_gross
    def _compute_transfers_net_gross(self):
        group = self.env.user.has_group("bd_net_gross_weight_on_all.group_net_gross_weight_delivery")
        for user in self:
            if group:
                user.transfers_net_gross = group in user.groups_id

    def _inverse_transfers_net_gross(self):
        group = [Command.link(self.env.ref('bd_net_gross_weight_on_all.group_net_gross_weight_delivery').id)]
        for user in self:
            if user.transfers_net_gross:
                self.env.user.sudo().group_ids = group
            else:
                self.env.user.sudo().group_ids = [(3, self.env.ref('bd_net_gross_weight_on_all.group_net_gross_weight_delivery').id)]

    # Repeat for invoicing_net_gross
    def _compute_invoicing_net_gross(self):
        group = self.env.user.has_group("bd_net_gross_weight_on_all.group_net_gross_weight_invoice")
        for user in self:
            if group:
                user.invoicing_net_gross = group in user.groups_id

    def _inverse_invoicing_net_gross(self):
        group = [Command.link(self.env.ref('bd_net_gross_weight_on_all.group_net_gross_weight_invoice').id)]

        for user in self:
            if user.invoicing_net_gross:
                self.env.user.sudo().group_ids = group
            else:
                self.env.user.sudo().group_ids = [(3, self.env.ref('bd_net_gross_weight_on_all.group_net_gross_weight_invoice').id)]
