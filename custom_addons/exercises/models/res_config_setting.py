from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    quotation_amount = fields.Integer(string='Amount to require quotation approval',
                                      config_parameter='sale.amount_to_require_quotation_approval')
    expected_ship_date = fields.Integer(string='Expected ship date', default=10,
                                        config_paramete='order.expected_ship_date')
