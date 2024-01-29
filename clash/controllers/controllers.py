# -*- coding: utf-8 -*-
# from odoo import http


# class Clash(http.Controller):
#     @http.route('/clash/clash', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/clash/clash/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('clash.listing', {
#             'root': '/clash/clash',
#             'objects': http.request.env['clash.clash'].search([]),
#         })

#     @http.route('/clash/clash/objects/<model("clash.clash"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('clash.object', {
#             'object': obj
#         })
