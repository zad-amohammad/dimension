from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dimension = fields.Char(related='product_id.dimension',store=True)
    sales_person = fields.Many2one('res.users',related='order_id.user_id')
