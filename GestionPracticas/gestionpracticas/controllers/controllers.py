# -*- coding: utf-8 -*-
# from odoo import http


# class Gestionpracticas(http.Controller):
#     @http.route('/gestionpracticas/gestionpracticas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestionpracticas/gestionpracticas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestionpracticas.listing', {
#             'root': '/gestionpracticas/gestionpracticas',
#             'objects': http.request.env['gestionpracticas.gestionpracticas'].search([]),
#         })

#     @http.route('/gestionpracticas/gestionpracticas/objects/<model("gestionpracticas.gestionpracticas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestionpracticas.object', {
#             'object': obj
#         })
