# -*- coding: utf-8 -*-
# from odoo import http


# class IccAnalBase(http.Controller):
#     @http.route('/icc_anal_base/icc_anal_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/icc_anal_base/icc_anal_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('icc_anal_base.listing', {
#             'root': '/icc_anal_base/icc_anal_base',
#             'objects': http.request.env['icc_anal_base.icc_anal_base'].search([]),
#         })

#     @http.route('/icc_anal_base/icc_anal_base/objects/<model("icc_anal_base.icc_anal_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('icc_anal_base.object', {
#             'object': obj
#         })
