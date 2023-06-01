# -*- coding: utf-8 -*-
# from odoo import http


# class Exercises(http.Controller):
#     @http.route('/exercises/exercises', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exercises/exercises/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exercises.listing', {
#             'root': '/exercises/exercises',
#             'objects': http.request.env['exercises.exercises'].search([]),
#         })

#     @http.route('/exercises/exercises/objects/<model("exercises.exercises"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exercises.object', {
#             'object': obj
#         })
