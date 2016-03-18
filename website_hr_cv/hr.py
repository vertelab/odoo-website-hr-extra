# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015- Vertel AB (<http://www.vertel.se>).
#
#    This progrupdateam is free software: you can redistribute it and/or modify
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
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning
import logging
from openerp import http
from openerp.http import request
_logger = logging.getLogger(__name__)

class hr_employee(models.Model):
    _inherit = 'hr.employee'

    @api.one
    def _assignment_tags(self):
        c0 = [item for sublist in self.assignment_ids.mapped(lambda r: r.categ_ids.mapped('id')) for item in sublist]
        c1 = [c for c in self.skill_ids.mapped('id')]
        self.all_categ_ids = [(6,_,set(c0+c1))]

    education = fields.Html(string='Educations', translate=True)
    assignment_ids = fields.One2many(comodel_name='hr.assignment', inverse_name='employee_id', string='Assignments')
    skill_ids = fields.One2many(comodel_name='hr.skill', inverse_name='employee_id', string='Skills')
    all_categ_ids = fields.Many2many(comodel_name='crm.case.categ', compute='_assignment_tags', string='All Tags')
    anonymous = fields.Boolean('Anonymous',help='Your CV can be published, but without your name and picture. Use this only if it is sensitive, given your current engagement')
    location_ids = fields.Many2many(comodel_name='hr.location', string='Places')
    language_ids = fields.Many2many(comodel_name='hr.language', string='Languages')

class hr_assignment(models.Model):
    _name = 'hr.assignment'

    name = fields.Char(string='name', translate=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    client = fields.Char(string='Client')
    categ_ids = fields.Many2many(comodel_name='crm.case.categ', string='Tags')
    description = fields.Html(string='Description')
    sequence = fields.Integer(string='Sequence')
    published = fields.Boolean(string='Published')
    date_from = fields.Date(string='Date from')
    date_to   = fields.Date(string='Date to')

class hr_skill(models.Model):
    _name='hr.skill'

    categ_id = fields.Many2one(comodel_name='crm.case.categ')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    level = fields.Selection([('1','< 1 year'),('2','1 - 3 years'),('3','3 - 5 years'),('4','> 5 years')], string='Level', required=False)

class hr_location(models.Model):
    _name='hr.location'

    name = fields.Char(string='Name', translate=True)

class hr_language(models.Model):
    _name='hr.language'

    name = fields.Char(string='Name', translate=True)


class website_hr(http.Controller):

    @http.route(['/consultants'], type='http', auth='public', website=True)
    def consultants(self, **post):
        return request.website.render("website_hr_cv.consultants_view",
            {'employee_ids': request.env['hr.employee'].sudo().search([],order="name")})

    @http.route(['/consultant/<model("hr.employee"):employee>'], type='http', auth="public", website=True)
    def consultant(self, employee,**post):
        return request.website.render("website_hr_cv.employee_view", {'employee': request.env['hr.employee'].sudo().browse(employee.id)})
