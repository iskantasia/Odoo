# # -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class type_request(models.Model) :
    _name = 'purchasing.type_request'
    _description = 'purchasing.type_request'
    _rec_name = 'type'

    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company"
    )
    company_name = fields.Char(related='employee_id.company_name')
    type = fields.Char()

class form_stationery(models.Model):
    _name = 'purchasing.stationery'
    _description = 'purchasing.stationery'
    # _order = 'date_order desc, id desc'
    _columns = {
        'code_pr': fields.Char(string='PR/', help="Auto Generate"),
        'code_product': fields.Char(string='CP/', help="Auto Generate")
    }

    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company"
    )

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
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')
    date_planned = fields.Datetime(string='Request Date', index=True)
    product_qty = fields.Float(comodel_name='product.lines', string='Quantity', index=True)

    # partner_id = fields.Many2one('res.partner', related='order_id.partner_id', string='Partner', readonly=True, store=True)
    # currency_id = fields.Many2one(related='order_id.currency_id', store=True, string='Currency', readonly=True)
    # date_order = fields.Datetime(related='order_id.date_planned', string='Order Date', readonly=True)

    # amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=True)
    # amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    # amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')

    # currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES, default=lambda self: self.env.company.currency_id.id)

#   Generate Code PR Auto
    code_pr = fields.Char(string="PR/", required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('PR/'))

    code_product = fields.Char(string="CP/", required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('CP/'))

#   Function for Generate Code PR
    @api.model
    def create(self, vals):
        if vals.get('code_pr', _('PR/')) == _('PR/'):
#   Untuk memanggil metode ORM langsung dari sebuah object
            vals['code_pr'] = self.env['ir.sequence'].next_by_code('purchasing.stationery.sequence') or _('PR/')
        result = super(form_stationery, self).create(vals)

    @api.model
    def create(self, vals):
        if vals.get('code_product', _('CP/')) == _('CP/'):
            vals['code_product'] = self.env['ir.sequence'].next_by_code('purchasing.stationery.sequence1') or _('CP/')
        result = super(form_stationery, self).create(vals)
        return result

    # @api.multi
    # def report(self):
    #     return self.env.ref('purchasing.stationery.report').report(self)
    #     self.filtered(lambda s: s.state == 'draft').write({'state' : 'sent'})
    #     return self.env.ref('purchasing.stationery.report')\
    #     .with_context({'discard_logo_check': True}).report_action(self)

class product_lines(models.Model):
    _name = 'product.lines'
    _description = 'product.lines'
    # _order = 'order_id'

    name = fields.Char(string='Product')
    product_name = fields.Many2one(comodel_name='purchasing.stationery', string='Product Name')
    code_pr = fields.Many2one(comodel_name='purchasing.stationery', string='PR/')
    code_product = fields.Many2one(comodel_name='purchasing.stationery', string='CP/')
    product_id = fields.Many2one(comodel_name='product.template', string='Name Product')
    date_planned = fields.Datetime(string='Request Date', index=True)

    # order_id = fields.Many2one('purchasing.stationery', string='Order Reference', index=True, required=True, ondelete='cascade')

    # price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    # price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    # price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

 #  ---------------------  Autofill / Join field product_uom, product_qty, price_unit by product_id  -----------------------
    product_qty = fields.Float(comodel_name='product.lines', string='Quantity', required=True)
    price_unit = fields.Many2one('res.currency', string='Unit Price', )
    product_uom = fields.Many2one('uom.uom', string='Unit Of Measure', default=lambda self: self.env['uom.uom'].search([]))
    # product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    # product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

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
            # lines = [(5, 0, 0)]
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
    # _inherit = purchasing.product_info
    _name = 'purchasing.product_info'
    _description = 'purchasing.product_info'
    # _inherit = 'purchasing.stationery'
    _columns = {
        'info_product': fields.Char('Information')
    }
    info_product = fields.Char(string='Information')
    state = fields.Char(string='Status')

class ProductProduct(models.Model):
    _inherit = 'product.product'
    # _columns = {
    #     'ket': fields.Char('Keterangan')
    # }
    keterangan = fields.Char(string='Keterangan')
