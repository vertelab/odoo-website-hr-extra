# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Enterprise Management Solution, third party addon
#    Copyright (C) 2014-2016 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, fields, models, _
# import odoo.tools
# import xmlrpclib
# from odoo.exceptions import Warning
# import os, string
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class HrEmployeeAcademy(models.Model):
    _inherit = 'hr.employee'

    chair_nbr = fields.Selection([('01', 'Stol nr 1'), ('02', 'Stol nr 2'), ('03', 'Stol nr 3'), ('04', 'Stol nr 4'), ('05', 'Stol nr 5'), ('06', 'Stol nr 6'), ('07', 'Stol nr 7'), ('08', 'Stol nr 8'), ('09', 'Stol nr 9'), (
        '10', 'Stol nr 10'), ('11', 'Stol nr 11'), ('12', 'Stol nr 12'), ('13', 'Stol nr 13'), ('14', 'Stol nr 14'), ('none', 'None'), ('emeritus', 'Emeritus'), ('adjungerad', 'Adjungerad')], string='Chair')
    emeritus_year = fields.Integer(
        string='Emeritus Year', help='The year became emeritus')
    public_info = fields.Text(string='Public Info')
    website_published = fields.Boolean(
        'Available in the website', copy=False, default=False)


class HrWebsite(http.Controller):

    @http.route('/academy/chairs', type='http', auth="public", website=True)
    def chairs_members(self, **post):
        employee_ids = request.env['hr.employee'].sudo().search([('chair_nbr', 'not in', [
            'none', 'emeritus']), ('website_published', '=', True)], order='chair_nbr')
        return request.render("website_hr_academy.chairs", {'employee_ids': employee_ids})

    @http.route(['/academy/member/<model("hr.employee"):employee>'], type='http', auth="public", website=True)
    def chair(self, employee, **post):
        employee = request.env['hr.employee'].sudo().browse(employee.id)
        return request.render("website_hr_academy.member", {'employee': employee})

    @http.route(['/academy/emeritus'], type='http', auth="public", website=True)
    def emeritus(self, **post):

        return request.render("website_hr_academy.chairs2", {'employee_ids': employee_ids})
            # "website_hr_academy.emeritus", {'emeritus': request.env['hr.employee'].sudo().search([('chair_nbr', '=', 'emeritus')], order='emeritus_year desc')})

    @http.route(['/academy/member/<model("hr.employee"):employee>/update'], type='http', auth="public", website=True)
    def update(self, employee, **post):
        if request.httprequest.method == 'POST':
            employee.sudo().write({
                'public_info': post.get('public_info'),
            })
            return request.render("website_hr_academy.member", {'employee': request.env['hr.employee'].sudo().browse(employee.id)})
        return request.render("website_hr_academy.update_member", {'employee': request.env['hr.employee'].sudo().browse(employee.id)})
