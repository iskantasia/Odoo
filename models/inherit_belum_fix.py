    # _inherit = 'product.lines'
    # _columns = {
    #     'product_info': fields.Char('Information', size=25, help="Example : Appartement 2 Tower")
    # }

    # def format_product_info(self, cr, uid, ids, product_info):
        # Memastikan User Menginput product_info
        # if npwp:
 
        # Mendefiniskan variabel result & warning
            # result = ''
            # warning = {"title": ("product_info Format Field Incorrect!"), "message": ("Masukan Keteragan tanpa tanda baca pada Product Information")}
 
            # Memeriksa jumlah karakter yang diinput berjumlah 25 
            # Jika tidak sesuai lemparkan warning error
            # if len(product_info) != 15 :
            #     return {'warning': warning, 'value': {'product_info': result}}
 
            # Memeriksa karakter yang diinput haruslah angka/number
            # Jika tidak sesuai lemparkan warning error
            # elif not product_info.isdigit():
            #     return {'warning': warning, 'value': {'product_info': result}}
 
            # Jika semua persayaratan telah benar, maka kita tambahkan separator product_info
            # Kita lemparkan format product_info yang sesuai
#             else:
#                 result = product_info[:2] + '.' + product_info[2:5] + '.' + product_info[5:8] + '.' + product_info[8] + '.' + product_info[9:12] + '-' + product_info[-3:] 
#                 return {'value': {'product_info': result}}
#         return True

# product_lines()


    # show_qtys = fields.Boolean(
    #     "Show Product Qtys", help="Show Product Qtys in POS", default=True
    # )
    # default_location_src_id = fields.Many2one(
    #     "stock.location", related="picking_type_id.default_location_src_id"
    # )

# ------------- Iherit
    # def get_info(self, name name=False, obj=False, pref=False, padding=6):
    #     sequence_id = self.env['ir.sequence'].search([
    #         ('name', '=', name),
    #         ('code', '=', code),
    #         ('prefix', '=', prefix),
    #     ])
    #     if not sequence_id :
    #         sequence_id = self.env['ir.sequence'].sudo().self.create({
    #             'name': name,
    #             'code': obj,
    #             'implementation': 'no_gap',
    #             'prefix' pref,
    #             'Draft': padding
    #         })
    #     return  sequence_id.next_by_id()

# <xpath expr="//field[@name='iface_big_scrollbars']/../.." position="after">
#                 <div class="col-xs-12 col-md-6 o_setting_box" id="show_prod_qtys">
#                     <div class="o_setting_left_pane">
#                         <field name="show_qtys" />
#                     </div>
#                     <div class="o_setting_right_pane">
#                         <label for="show_qtys" />
#                     </div>
#                 </div>
#             </xpath>
            
#             <field name="info_product" attrs="{'column_invisible': [('parent.state', 'not in', ['info_product', 'done'])]}"/>



# class feeder_data(osv.Model):
#     _name="feeder.data"
#     _columns = {
#         'product_id':fields.datetime('Char',),
#     }

# class data_value(osv.Model):
#     _name = "data.value"
#     _rec_name = "mega_wat"
#     _columns = {
#         'product_uom':field.related('combine', 'product_id',
#             type="Char", string="product_uom" )
#     }

# class feeder_data(osv.Model):
#     _name="feeder.data"
#     _columns = {
#         'date_of1':fields.datetime('Date',),
#     }

# class data_value(osv.Model):
#     _name = "data.value"
#     _rec_name = "mega_wat"
#     _columns = {
#         'time_read':fields.datetime('Time'),
#         # just add this to your code
#         'time_read_new':field.related('combine', 'date_of1',
#             type="datetime", string="Your Field Name" )
#     }



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