from odoo import models, fields, api, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = 'mail.thread'
    _description = 'Doctor Records'
    _rec_name = 'ref'

    name = fields.Char(string='Name', required=True, tracking=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("others", "Others")], string='Gender',
                              tracking=True)
    ref = fields.Char(string='Reference', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.doctor')
        return super(HospitalDoctor, self).create(vals_list)