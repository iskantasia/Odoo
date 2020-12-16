# # -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class type_request(models.Model) :
    _name = 'purchasing.type_request'
    _description = 'purchasing.type_request'
    _rec_name = 'type'

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
    
    # partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    # product_id form_purchasing
    # product_id = fields.Many2one('product.product', related='order_line.product_id', string='Product', readonly=False)

    product_id = fields.One2many(
        comodel_name='product.lines',
        inverse_name='product_name',
        string='Product'
        # required=True
    )

#   Autofill product_uom by product_id
    # product_uom = fields.One2many(
    #     comodel_name='product.lines',
    #     inverse_name='product_uom',
    #     string='Unit of Measure'
    #     # required=True
    # )

    # product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    # product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    # coordinator_id = fields.Many2one(comodel_name="res.partner", domain=[('function', '=', 'Coordinator')])
    # state = fields.Selection(string="State", selection=_state_state, default="lead")
    # active = fields.Boolean(string="Active", states={"closed": [("readonly", True)]})
    notes = fields.Text('Terms and Conditions')
    date_planned = fields.Datetime(string='Request Date', index=True)
    product_qty = fields.Float(comodel_name='product.lines', string='Quantity', index=True)

#   Generate Code PR Auto
    code_pr = fields.Char(string="Code PR", required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('New PR'))

    combination = fields.Char(string='Combination', compute='_compute_fields_combination')

#   Function for Generate Code PR
    @api.model
    def create(self, vals):
        if vals.get('code_pr', _('New PR')) == _('New PR'):
#   Untuk memanggil metode ORM langsung dari sebuah object
            vals['code_pr'] = self.env['ir.sequence'].next_by_code('purchasing.stationery.sequence') or _('New PR')
        result = super(form_stationery, self).create(vals)
        return result

    # @api.onchange("product_id")
    # def onchange_product_id(self):
    #     if self.product_id:
    #         name = self.product_id.name
    #         if self.product_id.code:
    #             name = "[{}] {}".format(name, self.product_id.code)
    #         if self.product_id.description_purchase:
    #             name += "\n" + self.product_id.description_purchase
    #         self.product_id = name

    # @models.depends('product_id', 'product_uom')
    # def _compute_fields_combination(self):
    #     for i in self:
    #         i.combination = i.product_id + ' ' + i.product_uom.name

#   api multi 1
    # @api.multi
    # def name_get(self):
    #     res = []
    #     for record in self:
    #         res.append((record.id, "%s %s" % (record.product_id, record.product_uom)))
    #     return res

#   api multi 2
    # @api.multi
    # def name_get(self):
    #     result = []
    #     for s in self:
    #         name = purchasing.product_id + ' ' + purchasing.product_uom
    #         result.append((s.id, name))
    #     return result

# Fungsi Print
    # @api.multi
    # def print_report(self):
    #     return self.env.ref('purchasing.staionery') \
    #         .with_context({'discard_logo_check': True}).report_action(self)

class product_lines(models.Model):
    _name = 'product.lines'
    _description = 'product.lines'

    name = fields.Char(string='Product')
    product_name = fields.Many2one(comodel_name='purchasing.stationery', string='Product Name')
    code_pr = fields.Many2one(comodel_name='purchasing.stationery', string='Code PR')
    product_id = fields.Many2one(comodel_name='product.template', string='Name Product')
    # product_id product_lines
    # product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True)
    product_qty = fields.Float(comodel_name='product.lines', string='Quantity', required=True)
    date_planned = fields.Datetime(string='Request Date', index=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
 #  Autofill / Join field product_uom by product_id
    # product_uom = fields.Many2one(comodel_name='uom.uom', string='Unit Of Measure')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    _sql_constraints = [
        ('accountable_required_fields',
            "CHECK(display_type IS NOT NULL OR (product_id IS NOT NULL AND product_uom IS NOT NULL AND date_planned IS NOT NULL))",
            "Missing required fields on accountable product lines."),
        ('non_accountable_null_fields',
            "CHECK(display_type IS NULL OR (product_id IS NULL AND product_uom IS NULL AND date_planned is NULL))",
            "Forbidden values on non-accountable purchase order line"),
    ]

    @api.depends('product_id')
    def _product_qty(self):
        for rec in self:
            if rec.product_id:
                rec.product_qty = rec.product_id.product_qty

    # @api.onchange('product_id')
    # def @api.onchange_product_id(self):
    #     for rec in self:
    #         # lines = [(5, 0, 0)]
    #         lines = []
    #         print("self.product_id")
    #         for line in self.product_id.:
    #             vals = {
    #                 'product_id': line.id,
    #                 'product_uom' 5
    #             }
    #             lines.append((0,0, vals))
    #         rec.form_purchasing = lines

    # @api.model
    # def create(self, values):
    #     if values.get('display_type', self.default_get(['display_type'])['display_type']):
    #     if values.get('product_uom'):
    #         values.update(product_id=False, product_qty=0, product_uom=False, date_planned=False)

    #     product_id = values.get('product_id')
    #     if 'date_planned' not in values:
    #         order = self.env['product.lines'].browse(product_id)
    #         if order.date_planned:
    #             values['date_planned'] = order.date_planned
    #     line = super(product_lines, self).create(values)
    #     return line

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            return

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.price_unit = self.product_qty = 0.0

        self._product_id_change()

        self._suggest_quantity()
        self._onchange_quantity()

# --------------------- Menu Product -----------------------
class ProductInfo(models.Model):
    _name = 'purchasing.product_info'
    _description = 'purchasing.product_info'
    # _inherit = 'purchasing.stationery'
    _columns = {
        'info_product': fields.Char('Information')
    }
    info_product = fields.Char(string='Information')
    state = fields.Char(string='Status')
