# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Dimension',
    'version' : '1.0',
    'depends' : ['base', 'product', 'sale_stock','stock', 'sale'],
    'data': [
        'views/product_template.xml',
        'views/sale_order_line.xml',
        'views/stock_picking.xml',
        'views/account_view_move_form.xml'
    ]
}
