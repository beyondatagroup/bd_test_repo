from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Product(models.Model):
    _inherit = "product.product"

    net_weight = fields.Float(string="Net Weight")
    gross_weight = fields.Float(string="Gross Weight")

    @api.onchange('net_weight', 'gross_weight')
    def _onchange_gross_weight(self):
        for product in self:
            if product.net_weight and product.gross_weight:
                if product.net_weight >= product.gross_weight:
                    raise ValidationError(
                        "Net Weight must be smaller than Gross Weight."
                    )


    # def write(self, vals):
    #     res = super().write(vals)
    #     print('---------------------vals-------------------',vals)
    #     print('---------------------res-------------------',res)

    #     if ('gross_weight' in vals or 'project_id' in vals):

    #     return res