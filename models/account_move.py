from odoo import api, fields, models, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    dimension = fields.Char(compute="_compute_order")

    @api.depends('account_id')
    def _compute_order(self):
        dim = None
        if self.move_id.line_ids.sale_line_ids.order_id.picking_ids:
            for move in self.move_id.line_ids.sale_line_ids.order_id.picking_ids[0].move_ids:
                if move.product_id.id == self.product_id.id:
                    dim = move.dimension
        self.dimension = dim
    
