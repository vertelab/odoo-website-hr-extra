''' Här definieras webbkontrollers – alltså HTTP-rutter för hemsidan.

@http.route(...)-dekorerade metoder.

Kod som:

hämtar data från modeller (t.ex. vilka anställda som fått rewards),

skickar data till en QWeb-template (definierad i views/website_academy_rewards.xml),

returnerar en webbsida.'''

from io import BytesIO
from odoo import models, fields, api, _
from odoo import SUPERUSER_ID
from odoo import http
#from odoo.addons.website.models.website import unslug
from odoo.tools.translate import _
from odoo.http import request
import werkzeug.urls
import base64

class WebsiteRewardees(http.Controller):
    _references_per_page = 20

 # Lista rewardees

    @http.route(['/rewardees', '/reward/<model("academy.reward"):reward>', '/reward/year/<int:year>'], type='http', auth="public", website=True)
    def rewardees(self, page=0, year=None, reward=None, **post):
        rewards = request.env['academy.reward'].sudo().search([], order='sequence_reward desc')
        if year:
            rewardees = request.env['academy.rewardee'].sudo().search([('reward_year', '=', year)], order='reward_year desc, sequence_rewardee desc')
        elif reward:
            rewardees = request.env['academy.rewardee'].sudo().search([('reward_id', '=', reward.id)], order='reward_year desc, sequence_rewardee desc')
        else:
            rewardees = request.env['academy.rewardee'].sudo().search([], order='reward_year desc, sequence_rewardee desc')
        return request.render("website_academy_rewards.index_rewardees", {'reward': reward, 'rewards': rewards, 'rewardees': rewardees, 'year': year})

    @http.route(['/rewardee/<model("academy.rewardee"):rewardee>'], type='http', auth="public", website=True)
    def rewardee(self, page=0, year=0, rewardee=None, **post):
        rewards = request.env['academy.reward'].sudo().search([], order='sequence_reward')
        return request.render("website_academy_rewards.index_rewardee", {'rewards': rewards, 'rewardee': request.env['academy.rewardee'].sudo().browse(rewardee.sudo().id),})

    @http.route(['/attachment/<model("ir.attachment"):attachment>/<string:file_name>'],
            type='http', auth="public", website=True)
    def get_attachment(self, attachment=None, file_name=None, **post):

        filecontent = attachment.raw
        filename = attachment.res_name.replace(' ', '_')

        headers = [
        ('Content-Type', attachment.mimetype),
        ('Content-Length', len(filecontent)),
        ('Content-Disposition', f'attachment; filename="{filename}"'),
        ]

        return request.make_response(filecontent, headers=headers)
