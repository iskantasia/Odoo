class ProductProduct(models.Model):
    _inherit = 'product.product'

    keterangan = fields.Char(string='Keterangan')
    purchased_product_qty = fields.Float(compute='_compute_purchased_product_qty', string='Purchased')

    # def _compute_purchased_product_qty(self):
    #     date_from = fields.Datetime.to_string(fields.datetime.now() - timedelta(days=365))
    #     domain = [
    #         ('state', 'in', ['purchase', 'done']),
    #         ('product_id', 'in', self.ids),
    #         ('date_order', '>', date_from)
    #     ]
    #     PurchaseOrderLines = self.env['purchase.order.line'].search(domain)
    #     order_lines = self.env['purchase.order.line'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id'])
    #     purchased_data = dict([(data['product_id'][0], data['product_uom_qty']) for data in order_lines])
    #     for product in self:
    #         if not product.id:
    #             product.purchased_product_qty = 0.0
    #             continue
    #         product.purchased_product_qty = float_round(purchased_data.get(product.id, 0), precision_rounding=product.uom_id.rounding)

    # def action_view_po(self):
    #     action = self.env.ref('purchase.action_purchase_order_report_all').read()[0]
    #     action['domain'] = ['&', ('state', 'in', ['purchase', 'done']), ('product_id', 'in', self.ids)]
    #     action['context'] = {
    #         'search_default_last_year_purchase': 1,
    #         'search_default_status': 1, 'search_default_order_month': 1,
    #         'graph_measure': 'qty_ordered'
    #     }
    #     return action

class ProductCategory(models.Model):
    _inherit = "product.category"

    property_account_creditor_price_difference_categ = fields.Many2one(
        'account.account', string="Price Difference Account",
        company_dependent=True,
        help="This account will be used to value price difference between purchase price and accounting cost.")

class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.onchange('name')
    def _onchange_name(self):
        self.currency_id = self.name.property_purchase_currency_id.id or self.env.company.currency_id.id