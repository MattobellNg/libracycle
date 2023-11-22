# -*- coding: utf-8 -*-
# from odoo import http


# class DelReadonly(http.Controller):
#     @http.route('/del_readonly/del_readonly', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/del_readonly/del_readonly/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('del_readonly.listing', {
#             'root': '/del_readonly/del_readonly',
#             'objects': http.request.env['del_readonly.del_readonly'].search([]),
#         })

#     @http.route('/del_readonly/del_readonly/objects/<model("del_readonly.del_readonly"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('del_readonly.object', {
#             'object': obj
#         })
