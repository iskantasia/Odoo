# # -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class type_request(models.Model) :
    _name = 'purchasing.type_request'
    _description = 'purchasing.type_request'
    _rec_name = 'type'

    type = fields.Char(string='type')
    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')
    company_name = fields.Char(related='employee_id.company_name')

class form_stationery(models.Model):
    _name = 'purchasing.stationery'
    _description = 'purchasing.stationery'
    _columns = {
        'code_pr': fields.Char(string='PR', help="Auto Generate")
    }

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')

    product_id = fields.One2many(
        comodel_name='product.lines',
        inverse_name='product_name',
        string='Product',
        required=True
    )

#   Autofill product_uom by product_id
    product_uom = fields.One2many(
        comodel_name='product.lines',
        inverse_name='product_uom',
        string='Unit of Measure',
        required=True
    )

    notes = fields.Text('Terms and Conditions')
    user_id = fields.Many2one('res.users', string=' Purchase Representative')
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")

    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')
    date_planned = fields.Datetime(string='Request Date', index=True)
    product_qty = fields.Many2one('product.lines', string='Quantity', index=True)
    date_from = fields.Datetime(string='From')
    date_to = fields.Date(sting='To')
    active = fields.Boolean('Active', default=True)
    date_order = fields.Datetime(string='Order Date', readonly=True)

    origin = fields.Char('Source Document', copy=False,
        help="Reference of the document that generated this purchase order "
             "request (e.g. a sales order)")

# -------------- compute='_amount_all' ---------------
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True)
    amount_total = fields.Monetary(string='Total', store=True, readonly=True)

    price_subtotal = fields.Monetary(string='Subtotal', store=True)
    # price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    # price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    invoice_count = fields.Integer(string='Bill Count', copy=False, default=0, store=True)
    invoice_ids = fields.Many2many('account.move', string='Bills', copy=False, store=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    base_currency_id = fields.Many2one('res.currency', default=lambda self: self.invoice_ids.company_id.currency_id.id)

    state = fields.Selection([
        ('draft', 'Purchase Request For Quotation'),   
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Stationery'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

#   Generate Code PR Auto
    code_pr = fields.Char(string="PR", required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('PR'))

#   Function for Generate Code PR
    @api.model
    def create(self, vals):
        if vals.get('code_pr', _('PR')) == _('PR'):
#   Untuk memanggil metode ORM langsung dari sebuah object
            vals['code_pr'] = self.env['ir.sequence'].next_by_code('purchasing.stationery.sequence') or _('PR')
        result = super(form_stationery, self).create(vals)
        return result

    def action_rfq_send(self):
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            if self.env.context.get('send_rfq', False):
                template_id = ir_model_data.get_object_reference('purchase', 'email_template_edi_purchase')[1]
            else:
                template_id = ir_model_data.get_object_reference('purchase', 'email_template_edi_purchase_done')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchasing.stationery',
            'active_model': 'purchasing.stationery',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })

        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            if template and template.lang:
                lang = template._render_template(template.lang, ctx['default_model'], ctx['default_res_id'])

        self = self.with_context(lang=lang)
        if self.state in ['draft', 'sent']:
            ctx['model_description'] = _('Request for Quotation')
        else:
            ctx['model_description'] = _('Purchase Order')

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    # @api.onchange('price_subtotal', 'invoice_ids.currency_id')
    # def compute_amount_total_currency(self):
    #     company_currency = self.invoice_ids.company_id.currency_id
    #     for l in self:
    #         amount_total = l.currency_id.compute(l.price_subtotal, company_currency)
    #         l.amount_total = amount_total

class product_lines(models.Model):
    _name = 'product.lines'
    _description = 'product.lines'

    name = fields.Char(string='Product')
    product_name = fields.Many2one(comodel_name='purchasing.stationery', string='Product Name')
    code_pr = fields.Many2one(comodel_name='purchasing.stationery', string='PR')
    product_id = fields.Many2one(comodel_name='product.template', string='Name Product')
    date_planned = fields.Datetime(string='Request Date', index=True)

 #  ---------------------  Autofill / Join field product_uom, product_qty, price_unit by product_id  -----------------------
    product_qty = fields.Float(string='Quantity', required=True)
    price_unit = fields.Many2one('res.currency', string='Unit Price', )
    product_uom = fields.Many2one('uom.uom', string='Unit Of Measure', default=lambda self: self.env['uom.uom'].search([]))

    currency_id = fields.Many2one(store=True, string='Currency', readonly=True)
    date_order = fields.Datetime(string='Order Date', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, readonly=True)

    _sql_constraints = [
        ('accountable_required_fields',
            "CHECK(display_type IS NOT NULL OR (product_id IS NOT NULL AND product_uom IS NOT NULL AND date_planned IS NOT NULL))",
            "Missing required fields on accountable purchase order line."),
        ('non_accountable_null_fields',
            "CHECK(display_type IS NULL OR (product_id IS NULL AND price_unit = 0 AND product_uom IS NULL AND date_planned is NULL))",
            "Forbidden values on non-accountable purchase order line"),
    ]

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            lines = []
            print("self.prduct_id", self.product_id.product_variant_ids)
            for line in self.product_id.product_variant_ids:
                val = {
                    'product_id': line.id,
                    'product_qty': 1,
                    'product_uom': line.id,
                    'unit_price': line.id
                }
                lines.append((0, 0, val))
            print("lines", lines)
            rec.product_lines = lines

# --------------------- Menu Product -----------------------
class ProductInfo(models.Model):
    _name = 'purchasing.product_info'

    info_product = fields.Char(string='Information')
    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')

# --------------------- Inherit Model Product -----------------------
class ProductProduct(models.Model):
    _inherit = 'product.product'
