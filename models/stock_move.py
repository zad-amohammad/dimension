from collections import  namedtuple
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models

class StockMove(models.Model):
    _inherit = "stock.move"

    dimension = fields.Char()


class StockRule(models.Model):
    _inherit = 'procurement.group'
    Procurement = namedtuple('Procurement', ['product_id', 'product_qty',
        'product_uom','dimension', 'location_id', 'name', 'origin', 'company_id', 'values'])

class StockRule(models.Model):
    _inherit = "stock.rule"

    

    def _get_stock_move_values(self, product_id, product_qty, product_uom,dimension, location_dest_id, name, origin, company_id, values):
        ''' Returns a dictionary of values that will be used to create a stock move from a procurement.
        This function assumes that the given procurement has a rule (action == 'pull' or 'pull_push') set on it.

        :param procurement: browse record
        :rtype: dictionary
        '''
        group_id = False
        if self.group_propagation_option == 'propagate':
            group_id = values.get('group_id', False) and values['group_id'].id
        elif self.group_propagation_option == 'fixed':
            group_id = self.group_id.id

        date_scheduled = fields.Datetime.to_string(
            fields.Datetime.from_string(values['date_planned']) - relativedelta(days=self.delay or 0)
        )
        date_deadline = values.get('date_deadline') and (fields.Datetime.to_datetime(values['date_deadline']) - relativedelta(days=self.delay or 0)) or False
        partner = self.partner_address_id or (values.get('group_id', False) and values['group_id'].partner_id)
        if partner:
            product_id = product_id.with_context(lang=partner.lang or self.env.user.lang)
        picking_description = product_id._get_description(self.picking_type_id)
        if values.get('product_description_variants'):
            picking_description += values['product_description_variants']
        # it is possible that we've already got some move done, so check for the done qty and create
        # a new move with the correct qty
        qty_left = product_qty

        move_dest_ids = []
        if not self.location_dest_id.should_bypass_reservation():
            move_dest_ids = values.get('move_dest_ids', False) and [(4, x.id) for x in values['move_dest_ids']] or []

        # when create chained moves for inter-warehouse transfers, set the warehouses as partners
        if not partner and move_dest_ids:
            move_dest = values['move_dest_ids']
            if location_dest_id == company_id.internal_transit_location_id:
                partners = move_dest.location_dest_id.warehouse_id.partner_id
                if len(partners) == 1:
                    partner = partners
                move_dest.partner_id = self.location_src_id.warehouse_id.partner_id or self.company_id.partner_id

        move_values = {
            'name': name[:2000],
            'company_id': self.company_id.id or self.location_src_id.company_id.id or self.location_dest_id.company_id.id or company_id.id,
            'product_id': product_id.id,
            'product_uom': product_uom.id,
            'dimension' : dimension,
            'product_uom_qty': qty_left,
            'partner_id': partner.id if partner else False,
            'location_id': self.location_src_id.id,
            'location_dest_id': location_dest_id.id,
            'move_dest_ids': move_dest_ids,
            'rule_id': self.id,
            'procure_method': self.procure_method,
            'origin': origin,
            'picking_type_id': self.picking_type_id.id,
            'group_id': group_id,
            'route_ids': [(4, route.id) for route in values.get('route_ids', [])],
            'warehouse_id': self.propagate_warehouse_id.id or self.warehouse_id.id,
            'date': date_scheduled,
            'date_deadline': False if self.group_propagation_option == 'fixed' else date_deadline,
            'propagate_cancel': self.propagate_cancel,
            'description_picking': picking_description,
            'priority': values.get('priority', "0"),
            'orderpoint_id': values.get('orderpoint_id') and values['orderpoint_id'].id,
            'product_packaging_id': values.get('product_packaging_id') and values['product_packaging_id'].id,
        }
        for field in self._get_custom_move_fields():
            if field in values:
                move_values[field] = values.get(field)
        return move_values

    

