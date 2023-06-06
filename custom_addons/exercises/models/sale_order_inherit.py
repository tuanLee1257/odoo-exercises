from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    deposit_required = fields.Boolean(string='Deposit Required')
    deposit_paid = fields.Boolean(string='Deposit Paid')
    deposit_paid_on = fields.Date(string='Deposit Paid On')
    deposit_ship_date = fields.Date(string='Deposit Ship Date', compute='_compute_ship_date')

    print_type = fields.Selection([('commercial', 'Commercial'), ('residential', 'Residential')], string='Type')

    approval_status = fields.Selection([('required', 'Waiting for approval'), ('approved', 'Approved')],
                                       string='Status', store=True, compute='_compute_require_approve', readonly=True)

    end_user = fields.Char(string='End User')

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

    @api.depends('amount_total')
    def _compute_require_approve(self):
        amount_for_approval = self.env['ir.config_parameter'].get_param('sale.amount_to_require_quotation_approval')
        float_amount_for_approval = float(amount_for_approval)
        for rec in self:
            if rec.amount_total > float_amount_for_approval:
                rec.approval_status = 'required'
            else:
                rec.approval_status = False

    @api.depends('approval_status')
    def _reload_quotation_state_on_approval_status(self):
        for rec in self:
            if rec.approval_status == 'required':
                rec.state = 'draft'

    def action_confirm_with_require_approval(self):
        self.action_confirm()
        for rec in self:
            if rec.approval_status == 'required':
                rec.state = 'draft'

    def action_confirm_quotation(self):
        self.action_unlock()

    def action_set_to_draft(self):
        self.action_draft()
