# -*- coding: utf-8 -*-

from odoo import models, fields, api

class type_request(models.Model) :
    _name = 'purchasing.type_request'
    _description = 'purchasing.type_request'
    _rec_name = 'type'

    type = fields.Char()

class form_stationery(models.Model):
    _name = 'purchasing.stationery'
    _description = 'purchasing.stationery'
    _rec_name = 'description'

    # perusahaan = fields.Selection([('K', 'Kawasan Industri Jababeka'), ('I', 'Indocargomas Persada'), (
    #     'G', 'Grahabuana Cikarang'), ('B', 'Bekasi Power'), ('M', 'Metropark Condominium Indah')], default='K')
    # jenis_permintaan = fields.Many2many('purchasing.type_request', string = "Jenis Permintaan")
    # dikeluarkan =  fields.Char(compute='_get_user')

    employee_id = fields.Many2one(comodel_name='res.partner', string='Employee')
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company"
    )

    product_id = fields.One2many(
        comodel_name='product.lines',
        inverse_name='product_name',
        string='Product'
    )

    date_planned = fields.Datetime(string='Request Date', index=True)
    product_qty = fields.Float(comodel_name='product.template', string='Quantity', index=True)
    product_uom = fields.One2many(
        comodel_name='product.lines',
        inverse_name='product_name',
        string='Unit of Measure'
    )

    description = fields.Text(string="Description")
    notes = fields.Text('Terms and Conditions')

    # def _get_user(self) :
    #     self.dikeluarkan = self.env.user.email

    # def approve(self) :
    #     self.diterima = self.env.user.email
    #     return {
    #       "type": "ir.actions.act_window",
    #       "view_mode": "tree,form",
    #       "res_model": "purchasing.stationery",
    #     }

class product_lines(models.Model):
    _name = 'product.lines'
    _description = 'product.lines'

    product_name = fields.Many2one(comodel_name='purchasing.stationery', string='Product')
    name = fields.Char(string='Product')
    product_id = fields.Many2one(comodel_name='product.template', string='Product')
    product_qty = fields.Float(comodel_name='product.template', string='Quantity', required=True)
    product_uom = fields.Many2one(comodel_name='uom.category', string='Unit Of Measure')
    # product_uom_category_id = fields.Many2one(related='product_id.product_uom_category_id.product_uom')
    date_planned = fields.Datetime(string='Request Date', index=True)
    description = fields.Text(string="Description")

    # uom_proud = fields.Char(related='product_id.product_uom.name', store=True)

    @api.depends('product_id')
    def _product_qty(self):
        for rec in self:
            if rec.product_id:
                rec.product_qty = rec.product_id.product_qty

#     @api.model
#     def oncreate(self):
#             self
