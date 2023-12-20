from odoo import fields, models

class StockMove(models.Model):
    _inherit = "stock.move"

    dimension = fields.Char(related="sale_line_id.dimension", store=True)

