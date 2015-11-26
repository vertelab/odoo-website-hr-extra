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

from cStringIO import StringIO
from openerp import models, fields, api, _
from openerp import SUPERUSER_ID
from openerp import http
from openerp.addons.website.models.website import unslug
from openerp.tools.translate import _
from openerp.http import request
import werkzeug.urls


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

    @api.one
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

    rewardee_ids = fields.One2many(comodel_name='academy.rewardee', inverse_name='partner_id', string='Prize')


class WebsiteRewardees(http.Controller):
    _references_per_page = 20

    @http.route(['/rewardees', '/reward/<model("academy.reward"):reward>', '/reward/year/<int:year>'], type='http', auth="public", website=True)
    def rewardees(self, page=0, year=None, reward=None, **post):
        rewards = request.env['academy.reward'].sudo().search([], order='sequence_reward')
        if reward:
            rewardees = request.env['academy.rewardee'].sudo().search([('reward_id', '=', reward.id)], order='sequence_rewardee')
        elif year:
            rewardees = request.env['academy.rewardee'].sudo().search([('reward_year', '=', year)], order='reward_year desc')
        else:
            rewardees = request.env['academy.rewardee'].sudo().search([], order='sequence_rewardee')
        return request.website.render("website_academy_rewards.index_rewardees", {'reward': reward, 'rewards': rewards, 'rewardees': rewardees, 'year': year})

    @http.route(['/rewardee/<model("academy.rewardee"):rewardee>'], type='http', auth="public", website=True)
    def rewardee(self, page=0, year=0, rewardee=None, **post):
        rewards = request.env['academy.reward'].sudo().search([], order='sequence_reward')
        return request.website.render("website_academy_rewards.index_rewardee", {'rewards': rewards, 'rewardee': request.env['academy.rewardee'].sudo().browse(rewardee.sudo().id),})

    @http.route(['/attachment/<model("ir.attachment"):attachment>/<string:file_name>'], type='http', auth="public", website=True)
    def get_attachment(self, attachment=None, file_name=None, **post):
        return http.send_file(StringIO(attachment.datas.decode('base64')), filename=attachment.datas_fname.replace(' ', '_'), mimetype=attachment.mimetype, mtime=attachment.write_date, as_attachment=True)


#     @http.route([
#         '/rewardees',
#         '/rewardees/page/<int:page>',
#         '/rewardees/country/<int:country_id>',
#         '/rewardees/country/<country_name>-<int:country_id>',
#         '/rewardees/country/<int:country_id>/page/<int:page>',
#         '/rewardees/country/<country_name>-<int:country_id>/page/<int:page>',
#     ], type='http', auth="public", website=True)
#     def rewardees(self, country_id=0, page=0, country_name='', **post):
#         cr, uid, context = request.cr, request.uid, request.context
#         country_obj = request.registry['res.country']
#         partner_obj = request.registry['res.partner']
#         partner_name = post.get('search', '')
#
#         domain = [('website_published', '=', True), ('assigned_partner_id', '!=', False)]
#         if partner_name:
#             domain += [
#                 '|',
#                 ('name', 'ilike', post.get("search")),
#                 ('website_description', 'ilike', post.get("search"))
#             ]
#
#         # group by country, based on customers found with the search(domain)
#         countries = partner_obj.read_group(
#             cr, openerp.SUPERUSER_ID, domain, ["id", "country_id"],
#             groupby="country_id", orderby="country_id", context=request.context)
#         country_count = partner_obj.search(
#             cr, openerp.SUPERUSER_ID, domain, count=True, context=request.context)
#
#         if country_id:
#             domain += [('country_id', '=', country_id)]
#             if not any(x['country_id'][0] == country_id for x in countries if x['country_id']):
#                 country = country_obj.read(cr, uid, country_id, ['name'], context)
#                 if country:
#                     countries.append({
#                         'country_id_count': 0,
#                         'country_id': (country_id, country['name'])
#                     })
#                 countries.sort(key=lambda d: d['country_id'] and d['country_id'][1])
#
#         countries.insert(0, {
#             'country_id_count': country_count,
#             'country_id': (0, _("All Countries"))
#         })
#
#         # search customers to display
#         partner_count = partner_obj.search_count(cr, openerp.SUPERUSER_ID, domain, context=request.context)
#
#         # pager
#         url = '/customers'
#         if country_id:
#             url += '/country/%s' % country_id
#         pager = request.website.pager(
#             url=url, total=partner_count, page=page, step=self._references_per_page,
#             scope=7, url_args=post
#         )
#
#         partner_ids = partner_obj.search(request.cr, openerp.SUPERUSER_ID, domain,
#                                          offset=pager['offset'], limit=self._references_per_page,
#                                          context=request.context)
#         google_map_partner_ids = ','.join(map(str, partner_ids))
#         partners = partner_obj.browse(request.cr, openerp.SUPERUSER_ID, partner_ids, request.context)
#
#         values = {
#             'countries': countries,
#             'current_country_id': country_id or 0,
#             'partners': partners,
#             'google_map_partner_ids': google_map_partner_ids,
#             'pager': pager,
#             'post': post,
#             'search_path': "?%s" % werkzeug.url_encode(post),
#         }
#         return request.website.render("website_customer.index", values)
#
#     # Do not use semantic controller due to SUPERUSER_ID
#     @http.route(['/rewardee/<model("res.partner"):partner>'], type='http', auth="public", website=True)
#     def partners_detail(self, partner, **post):
#         return request.website.render("website_academy_reward.details", {'partner': partner})
