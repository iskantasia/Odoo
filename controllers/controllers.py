# -*- coding: utf-8 -*-
# from odoo import http


# class Purchasing(http.Controller):
#     @http.route('/purchasing/purchasing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchasing/purchasing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchasing.listing', {
#             'root': '/purchasing/purchasing',
#             'objects': http.request.env['purchasing.purchasing'].search([]),
#         })

#     @http.route('/purchasing/purchasing/objects/<model("purchasing.purchasing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchasing.object', {
#             'object': obj
#         })
