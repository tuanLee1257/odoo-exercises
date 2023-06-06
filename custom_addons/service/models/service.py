from odoo import models, fields, api, _


class Service(models.Model):
    _name = 'service.service'
    _description = 'Service'

    name = fields.Char(string='Name')
    parent = fields.Many2one('service.service', string='Parent')
    hourly_cost = fields.Float(string='Hourly cost')
    margin = fields.Float(string='Margin')
