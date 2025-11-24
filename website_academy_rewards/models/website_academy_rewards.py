# -*- coding: utf-8 -*-
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

#from cStringIO import StringIO
from io import BytesIO
from odoo import models, fields, api, _
from odoo import SUPERUSER_ID
from odoo import http
#from odoo.addons.website.models.website import unslug
from odoo.tools.translate import _
from odoo.http import request
import werkzeug.urls
import base64


class academy_reward(models.Model):  # prize
    _name = "academy.reward"

    name = fields.Char(string='Prize Name')
    rewardee_ids = fields.One2many(comodel_name='academy.rewardee', inverse_name='reward_id', string='Winners')
    description = fields.Text(string='Description')
    sequence_reward = fields.Integer(string='Sequence')

    @api.model
    def get_years(self):
        rewardees = self.env['academy.rewardee'].search([], order='reward_year desc')
        years = []
        for r in rewardees:
            if r.reward_year not in years:
                years.append(r.reward_year)

        return years

class academy_rewardee(models.Model):  # who took prize
    _name = "academy.rewardee"
    _order = "reward_year desc, sequence_rewardee desc"

    # ~ @api.one
    def _name_(self):
        self.name = '%s - %s' % (self.reward_id.name, self.reward_year)

    name = fields.Char(compute='_name_', string='Name')
    reward_year = fields.Integer(string='Year')
    sequence_rewardee = fields.Integer(string='Sequence')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Winner')
    reward_id = fields.Many2one(comodel_name='academy.reward', string='Prize')
    comment = fields.Text(string='Justification')

    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     return super('academy.rewardee', self).name


class res_partner(models.Model):
    _inherit = "res.partner"

    rewardee_ids = fields.One2many(comodel_name='academy.rewardee', inverse_name='partner_id', string='Rewardee')
    press_id = fields.Many2one(comodel_name='blog.post', string='Press')


class BlogPost(models.Model):
    _inherit = "blog.post"

    partner_ids = fields.One2many(comodel_name='res.partner', inverse_name='press_id', string='Rewardee')
