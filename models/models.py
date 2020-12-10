# # -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from xlrd import open_workbook
# import base64
# import xlrd
# import tempfile

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
    # _order = 'date_order desc, id desc'
    _columns = {
        'code_pr': fields.Char(string='PR', help="Auto Generate")
        # 'code_product': fields.Char(string='CP/', help="Auto Generate")
    }

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    # import_xls = fields.Binary('File')
    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')

    # company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.company.id)

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
    product_qty = fields.Many2one('product.lines', string='Quantity', index=True)
    date_from = fields.Datetime(string='From')
    date_to = fields.Date(sting='To')
    # image = field.Binary(string="Image")
    active = fields.Boolean('Active', default=True)

    # partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    # partner_id = fields.Many2one('res.partner', related='order_id.partner_id', string='Partner', readonly=True, store=True)
    # dest_address_id = fields.Many2one('res.partner', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", string='Drop Ship Address', states=READONLY_STATES,
    #     help="Put an address if you want to deliver directly from the vendor to the customer. "
    #         "Otherwise, keep empty to deliver to your own company.")
    # currency_id = fields.Many2one(related='order_id.currency_id', store=True, string='Currency', readonly=True)
    # date_order = fields.Datetime(related='order_id.date_planned', string='Order Date', readonly=True)

    # amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=True)
    # amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    # amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')

    # currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES, default=lambda self: self.env.company.currency_id.id)

    state = fields.Selection([
        ('draft', 'RFQ'),   
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    # state = fields.Many2one(comodel_name='purchasing.product_info', string='State', store=True)
    order_line = fields.One2many('purchase.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

#   Generate Code PR Auto
    code_pr = fields.Char(string="PR", required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('PR'))

    # code_product = fields.Char(string="CP/", required=True, copy=False, readonly=True,
    #                       index=True, default=lambda self: _('CP/'))
    # @api.depends('')
    # def set__group(self):
    #     for rec in self:
    #         if rec._:
    #             if ._ < 18:
    #                 rec._group = 'min'
    #             else:
    #                 rec._group = 'max'

    # def open__(self):
    #     print("")
    
    # def records_import(self, cr, uid, ids, context=None):
    #     supplier_obj = self.pool.get('res.partner')
    #     for price in self.browse(cr, uid, ids, context=context):
    #         fileName, fileExtension = os.path.splitext(price.file_to_import_fname)
    #         if fileExtension != '.csv':
    #             raise osv.except_osv(_("Warning !"), _("Change the file type as CSV"))
    #         price_file = unicode(base64.decodestring(price.import_payment), 'windows-1252', 'strict').split('\n')
    #         line_count = 0
    #         ss = len(price_file)
    #         for line in price_file:
    #             line_count += 1
    #             if line_count > 1:
    #                 if  line_count < ss -1:
    #                     line_contents = line.split(',')
    #                     if not line_contents:
    #                         break
    #                     Name = line_contents[0].strip()
    #                     Amount = line_contents[1].strip()
    #                     supplier_id = supplier_obj.search(cr, uid, [('name', '=', Name)])
    #                     if supplier_id == []:
    #                         supplier = {
    #                             'name':Name
    #                         }
    #                         new_supplier = supplier_obj.create(cr, uid, supplier)
    #                     else:
    #                         for supp in supplier_obj.browse(cr, uid, supplier_id):
    #                             new_supplier = supp.id
    #                     price_line_exist = self.pool.get('sample.lines').search(cr, uid, [('name', '=', new_supplier),('payment_id', '=', price.id),('amount', '=', Amount)])
    #                     if price_line_exist == []:
    #                         price_upload_dict = {
    #                                                 'name' : new_supplier,
    #                                                 'amount': Amount
    #                                             }
    #                         self.pool.get('sample.lines').create(cr, uid, price_upload_dict)
    #         self.write(cr, uid, price.id,{'upload':True},context=context)
    #     return {}

    # def import_xls(self):
    #      wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
    #      for sheet in wb.sheets():
    #          for row in range(sheet.nrows):
    #              for col in range(sheet.ncols):
    #                  print  (sheet.cell(row,col).value)

    # def import_data(self, cr, uid, ids, context=None):
    #     temp_path = tempfile.gettempdir()
    #     test_obj = self.pool.get('test.test')
    #     xls_data = base64.decodestring(xls_file)
    #     fp=open(temp_path+'/xsl_file.xls', 'wb+')
    #     fp.write(xls_data)
    #     fp.close()
    #     wb = open_workbook(temp_path+'/xsl_file.xls')
    #     for sheet in wb.sheets():
    #         for rownum in range(sheet.nrows):
    #             if rownum == 0:
    #                 header_list = sheet.row_values(rownum)

#   Function for Generate Code PR
    @api.model
    def create(self, vals):
        if vals.get('code_pr', _('PR')) == _('PR'):
#   Untuk memanggil metode ORM langsung dari sebuah object
            vals['code_pr'] = self.env['ir.sequence'].next_by_code('purchasing.stationery.sequence') or _('PR')
        result = super(form_stationery, self).create(vals)

    # @api.model
    # def create(self, vals):
    #     if vals.get('code_product', _('CP/')) == _('CP/'):
    #         vals['code_product'] = self.env['ir.sequence'].next_by_code('purchasing.stationery.sequence1') or _('CP/')
    #     result = super(form_stationery, self).create(vals)
        return result

# --------------------------------- Print / Report ---------------------------------
    # @api.multi
    # def report(self):
    #     return self.env.ref('purchasing.stationery.report').report(self)
    #     self.filtered(lambda s: s.state == 'draft').write({'state' : 'sent'})
    #     return self.env.ref('purchasing.stationery.report')\
    #     .with_context({'discard_logo_check': True}).report_action(self)

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

        # In the case of a RFQ or a PO, we want the "View..." button in line with the state of the
        # object. Therefore, we pass the model description in the context, in the language in which
        # the template is rendered.
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

class product_lines(models.Model):
    _name = 'product.lines'
    _description = 'product.lines'
    # _order = 'order_id'

    name = fields.Char(string='Product')
    product_name = fields.Many2one(comodel_name='purchasing.stationery', string='Product Name')
    code_pr = fields.Many2one(comodel_name='purchasing.stationery', string='PR')
    # code_product = fields.Many2one(comodel_name='purchasing.stationery', string='CP/')
    product_id = fields.Many2one(comodel_name='product.template', string='Name Product')
    date_planned = fields.Datetime(string='Request Date', index=True)

    # order_id = fields.Many2one('purchasing.stationery', string='Order Reference', index=True, required=True, ondelete='cascade')

    # price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    # price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    # price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

 #  ---------------------  Autofill / Join field product_uom, product_qty, price_unit by product_id  -----------------------
    product_qty = fields.Float(string='Quantity', required=True)
    price_unit = fields.Many2one('res.currency', string='Unit Price', )
    product_uom = fields.Many2one('uom.uom', string='Unit Of Measure', default=lambda self: self.env['uom.uom'].search([]))

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
    _name = 'purchasing.product_info'

    # name = fields.Char(store="True")
    # name = fields.Char(compute='_compute_name', store="True")
    info_product = fields.Char(string='Information')
    # state = fields.Char(string='State', store=True)
    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')

    # @api.depends('info_product','state')
    # def _compute_name(self):
    #     for record in self:
    #         record.name = str(record.info_product)+str(record.state)

#     @api.model
#     def create(self, vals):
#         if vals.get('info_product', _('New')) == _('New'):
#             vals['info_product'] = self.env['ir.sequence_info'].next_by_code('purchasing.product_info.sequence_info') or _('New')
#         result = super(ProductInfo, self).create(vals)

    # def onchange_info_state(self, cr, uid, ids, info_product, state, context=None):
    #     v = {}
    #     if info_product and state:
    #         v['name'] = info_product+state
    #     return {'value': v}

    # @api.model
    # def create(self, vals):
    #     if vals['info_product']:
    #         info_product = vals['info_product'].title()
    #     else:
    #         info_product = ''
    #     if vals['state']:
    #         state = vals['state'].title()
    #     else:
    #         state = ''
    #         name = "{}, {}".format(state, info_product,)
    #     print 'name', name
    #         vals['name'] = name
    #         vals['info_product'] = info_product
    #         vals['state'] = state
    #     if 'address_id' in vals:
    #         res_id = super(HrEmployee, self).create(vals)
    #     return res_id
        # return

# --------------------- Inherit Model Product -----------------------
class ProductProduct(models.Model):
    _inherit = 'product.product'

    # infoproduct = fields.Many2one('purchasing.product_info', string='Info Product')
    # state_product = fields.Char(related='infoproduct.state_product', string='State Product')

# class PurchaseOrder(models.Model):
#     _name = "purchase.order"
#     _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
#     _description = "Purchase Order"
#     _order = 'date_order desc, id desc'

    # @api.depends('order_line.price_total')
    # def _amount_all(self):
    #     for order in self:
    #         amount_untaxed = amount_tax = 0.0
    #         for line in order.order_line:
    #             line._compute_amount()
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #         order.update({
    #             'amount_untaxed': order.currency_id.round(amount_untaxed),
    #             'amount_tax': order.currency_id.round(amount_tax),
    #             'amount_total': amount_untaxed + amount_tax,
    #         })
