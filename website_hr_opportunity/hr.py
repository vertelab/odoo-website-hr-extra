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


class crm_lead(models.Model):
    """ CRM Lead Case """
    _inherit = "crm.lead"

    website_published = fields.Boolean('Published')
    public_info = fields.Text('Public info',translate=True)
    public_client = fields.Char('Public CLient')
    location = fields.Many2one(comodel_name='hr.location')
    duration = fields.Integer()
    duration_uom = field.Many2one(comodel_name='product.oum')
    work_load = fields.Integer('Workload in %',help="for example 100% or 50%")
    start_date = fields.Date()
    language_skills = fields.Many2one(comodel_name='hr.language')
    skill_ids = fields.Many2many()
    
class lead_skill(models.Model):
    _name="crm.lead.skill"
    categ_id = fields.Many2one(comodel_name='crm.case.categ')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    level = fields.Selection([('1','1 - 3 year'),('2','3 - 5 year'),('3','5 - more years')], string='Level', required=False)
    prio = fields.Selection([('0','Required'),('1','High'),('2','Medium'),('3','Not required')], string='Prio', required=False)
    
class hr(osv.osv):
    _inherit = 'hr.employee'
    _columns = {
        'website_published': fields.boolean('Available in the website', copy=False),
        'public_info': fields.text('Public Info'),
    }
    _defaults = {
        'website_published': False
    }



class hr_employee(models.Model):
    _inherit = 'hr.employee'

    def _assignment_tags(self):
        self.all_categ_ids = (6,_,sorted(set([c.name for c in a.categ_ids for a in self.assignment_ids]+
                                             [c.name for c in self.categ_ids])))

    education = fields.Html(string='Educations', translate=True)
    assignment_ids = fields.One2many(comodel_name='hr.assignment', inverse_name='employee_id', string='Assignments')
    categ_ids = fields.Many2many(comodel_name='crm.case.categ', string='Tags')
    all_categ_ids = fields.Many2many(compute='_assignment_tags', string='All Tags')
    anonymous = fields.Boolean('Anonymous',help="Your CV can be published, but without your name and picture. Use this only if it is sensitive, given your current engagement")

class hr_assignment(models.Model):
    _name = 'hr.assignment'

    name = fields.Char(string='name', translate=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    client = fields.Char(string='Client')
    categ_ids = fields.Many2many(comodel_name='crm.case.categ', string='Tags')
    description = fields.Html(string='Description')
    sequence = fields.Integer(string='Sequence')
    published = fields.Boolean(string='Published')
    place_ids = fields.Many2many(comodel_name='hr.place', string='Places')
    date_from = fields.Date()
    date_to   = fields.Date()
    
    
class hr_place(models.Model):
    _name="hr.place"
    name = fields.Char(string='name', translate=True)
    

class website_hr(http.Controller):

    @http.route(['/consultants'], type='http', auth="public", website=True)
    def consultants(self, **post):
        return request.website.render("website_hr_cv.consultants_view",
            {'employee_ids': request.env['hr.employee'].sudo().search([],order="name")})

    @http.route(['/consultant/<model("hr.employee"):employee>'], type='http', auth="public", website=True)
    def consultant(self, employee,**post):
        return request.website.render("website_hr_cv.employee_view", {'employee': request.env['hr.employee'].sudo().browse(employee.id)})

