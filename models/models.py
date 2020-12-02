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
    # _rec_name = 'combination'
    _columns = {
        'code_pr': fields.Char(string='PR Code', help="Auto Generate")
    }

    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company"
    )
    # company_id = fields.Char(related='employee_id.company_id')

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

#   Generate Code PR Auto
    code_pr = fields.Char(string="Code PR", required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('New PR'))

#   Function for Generate Code PR
    @api.model
    def create(self, vals):
        if vals.get('code_pr', _('New PR')) == _('New PR'):
#   Untuk memanggil metode ORM langsung dari sebuah object
            vals['code_pr'] = self.env['ir.sequence'].next_by_code('purchasing.stationery.sequence') or _('New PR')
        result = super(form_stationery, self).create(vals)
        return result

class product_lines(models.Model):
    _name = 'product.lines'
    _description = 'product.lines'
    # _order = 'order_id'

    name = fields.Char(string='Product')
    product_name = fields.Many2one(comodel_name='purchasing.stationery', string='Product Name')
    code_pr = fields.Many2one(comodel_name='purchasing.stationery', string='Code PR')
    product_id = fields.Many2one(comodel_name='product.template', string='Name Product')
    product_qty = fields.Float(comodel_name='product.lines', string='Quantity', required=True)
    date_planned = fields.Datetime(string='Request Date', index=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
 #  Autofill / Join field product_uom by product_id
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
                    'product_uom': line.uom_id
                }
                lines.append((0, 0, val))
            print("lines", lines)
            rec.product_lines = lines

#
    # @api.onchange('product_id')
    # def onchange_product_id(self):
    #     if not self.product_id:
    #         return

    #     Reset date, price and quantity since _onchange_quantity will provide default values

#
    #     self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
    #     self.price_qty = self.product_uom = 0.0

    #     self._product_id_change()

    #     self._suggest_quantity()
    #     self._onchange_quantity()

    # def _product_id_change(self):
    #     if not self.product_id:
    #         return
#
    # @api.onchange('product_qty', 'product_uom')
    # def _onchange_quantity(self):
    #     if not self.product_id:
    #         return
        # params = {'order_id': self.order_id}
        # seller = self.product_id._select_seller(
        #     partner_id=self.partner_id,
        #     quantity=self.product_qty,
        #     date=self.order_id.date_order and self.order_id.date_order.date(),
        #     uom_id=self.product_uom,
        #     params=params)

        # if seller or not self.date_planned:
        #     self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        # if not seller:
        #     if self.product_id.seller_ids.filtered(lambda s: s.name.id == self.partner_id.id):
        #         self.price_unit = 0.0
        #     return

        # price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
        # if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
        #     price_unit = seller.currency_id._convert(
        #         price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

        # if seller and self.product_uom and seller.product_uom != self.product_uom:
        #     price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        # self.price_unit = price_unit

    # @api.depends('product_uom', 'product_qty', 'product_id')
    # def _compute_product_qty(self):
    #     for line in self:
    #         if line.product_id and line.product_id.uom_id != line.product_uom:
    #             line.product_qty = line.product_uom._compute_quantity(line.product_qty, line.product_id.uom_id)
    #         else:
    #             line.product_qty = line.product_qty

#
    # def _suggest_quantity(self):
    #     '''
    #     Suggest a minimal quantity based on the buy
    #     '''
    #     if not self.product_id:
    #         return
        # seller_min_qty = self.product_id.seller_ids\
        #     .filtered(lambda r: r.name == self.order_id.partner_id and (not r.product_id or r.product_id == self.product_id))\
        #     .sorted(key=lambda r: r.min_qty)
        # if seller_min_qty:
        #     self.product_qty = seller_min_qty[0].min_qty or 1.0
        #     self.product_uom = seller_min_qty[0].product_uom
        # else:
        #     self.product_qty = 1.0
#
#       return name
        # return {
        #     'product_uom': self.product_uom.id,
        #     'product_id': self.product_id.id
        # }

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
