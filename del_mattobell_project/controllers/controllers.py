# -*- coding: utf-8 -*-
# from odoo import http


# class DelMattobellProject(http.Controller):
#     @http.route('/del_mattobell_project/del_mattobell_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/del_mattobell_project/del_mattobell_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('del_mattobell_project.listing', {
#             'root': '/del_mattobell_project/del_mattobell_project',
#             'objects': http.request.env['del_mattobell_project.del_mattobell_project'].search([]),
#         })

#     @http.route('/del_mattobell_project/del_mattobell_project/objects/<model("del_mattobell_project.del_mattobell_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('del_mattobell_project.object', {
#             'object': obj
#         })
