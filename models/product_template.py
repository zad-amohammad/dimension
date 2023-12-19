from odoo import fields, api, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    dimension = fields.Char()
