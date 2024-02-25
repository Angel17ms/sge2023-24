# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import Request


class YourController(http.Controller):

    @http.route('/jsonrpc', type='json', auth='none', methods=['POST'], csrf=False)
    def your_jsonrpc_handler(self, **kw):
        db = http.request.env['res.users']
        users = db.search([])  # Obtener todos los registros de res.users
        user_data = []
        for user in users:
            user_data.append({
                'name': user.name,
                'password': user.password,
                'is_premium': user.is_premium,
                'karma': user.karma,
            })
        return {'result': user_data}

#     @http.route('/proyecto/proyecto/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('proyecto.listing', {
#             'root': '/proyecto/proyecto',
#             'objects': http.request.env['proyecto.proyecto'].search([]),
#         })

#     @http.route('/proyecto/proyecto/objects/<model("proyecto.proyecto"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proyecto.object', {
#             'object': obj
#         })
