from odoo import api, fields, models, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    dimension = fields.Char(compute="_compute_order")

    @api.depends('account_id')
    def _compute_order(self):
        dim = None
        pickings =self.move_id.line_ids.sale_line_ids.order_id.picking_ids
        if pickings:
            pickings = [ picking for picking in pickings if picking.state != 'cancel' ]
            if pickings:
                for move in pickings[-1].move_ids:
                    if move.product_id.id == self.product_id.id:
                        dim = move.dimension
        self.dimension = dim
    
