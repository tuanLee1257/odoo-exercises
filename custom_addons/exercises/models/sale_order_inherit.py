from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    deposit_required = fields.Boolean(string='Deposit Required')
    deposit_paid = fields.Boolean(string='Deposit Paid')
    deposit_paid_on = fields.Date(string='Deposit Paid On')
    deposit_ship_date = fields.Date(string='Deposit Ship Date', compute='_compute_ship_date')

    print_type = fields.Selection([('commercial', 'Commercial'), ('residential', 'Residential')], string='Type')
    approved = fields.Boolean(string='Is Approved?')
    require_approve = fields.Boolean(string='Require approve', store=True, compute='_compute_require_approve')
    approval_status = fields.Selection([('required', 'Waiting for approval'), ('approved', 'Approved')],
                                       string='Status')
    end_user = fields.Char(string='End User')
    end_user_related_id = fields.Many2one(
        'res.partner',
        string='End User Related',
        compute='_compute_end_user_related'
    )

    @api.onchange('deposit_paid')
    def _onchange_deposit_paid(self):
        for rec in self:
            if not rec.deposit_paid:
                rec.deposit_paid_on = False
            else:
                rec.deposit_paid_on = fields.Datetime.now()

    @api.depends('deposit_paid_on')
    def _compute_ship_date(self):
        for rec in self:
            if not rec.deposit_paid_on:
                rec.deposit_ship_date = False
            else:
                paid_date = fields.Datetime.from_string(rec.deposit_paid_on)
                ship_date = paid_date + relativedelta(weeks=7)
                rec.deposit_ship_date = ship_date.date()

    def _compute_end_user_related(self):
        for order in self:
            order.end_user_related_id = self.env['res.partner'].search(
                [('name', 'ilike', order.end_user)], limit=1
            )

    @api.depends('amount_total')
    def _compute_require_approve(self):
        amount_for_approval = self.env['ir.config_parameter'].get_param('sale.amount_to_require_quotation_approval')
        float_amount_for_approval = float(amount_for_approval)
        if self.amount_total > float_amount_for_approval:
            self.approval_status = 'required'

    def action_redirect_to_customer(self):
        return {
            'name': ('Redirect Chosen Products'),
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'sale.order',
            'target': 'current',
            'view_id': False,
            # 'domain': [('id', 'in', ids)]  # Filter id barang yang ditampilkan
        }
