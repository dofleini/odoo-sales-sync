# -*- coding: utf-8 -*-
# from odoo import http


# class GoogleCloudSender(http.Controller):
#     @http.route('/google_cloud_sender/google_cloud_sender/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/google_cloud_sender/google_cloud_sender/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('google_cloud_sender.listing', {
#             'root': '/google_cloud_sender/google_cloud_sender',
#             'objects': http.request.env['google_cloud_sender.google_cloud_sender'].search([]),
#         })

#     @http.route('/google_cloud_sender/google_cloud_sender/objects/<model("google_cloud_sender.google_cloud_sender"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('google_cloud_sender.object', {
#             'object': obj
#         })
