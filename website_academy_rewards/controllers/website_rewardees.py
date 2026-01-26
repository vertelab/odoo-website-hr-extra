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
# from odoo.addons.website.models.website import unslug
from odoo.tools.translate import _
from odoo.http import request
import werkzeug.urls
import base64
from datetime import date


class WebsiteRewardees(http.Controller):
    _references_per_page = 20

    # Lista rewardees
    @http.route(
        ['/rewardees', '/reward/<model("academy.reward"):reward>', '/reward/year/<int:year>', '/reward/<model("academy.reward"):reward>/year/<int:year>'],
        type='http', auth="public", website=True
    )
    def rewardees(self, page=0, year=None, reward=None, **post):
        year = int(year) if year else date.today().year

        # Visa ALLA utmärkelser
        rewards = request.env['academy.reward'].sudo().search([], order='sequence_reward asc')

        if year and reward:
            rewardees = request.env['academy.rewardee'].sudo().search(
                [('reward_year', '=', year), ('reward_id', '=', reward.id)],
                order='reward_year desc, sequence_rewardee asc'
            )
        elif year:
            rewardees = request.env['academy.rewardee'].sudo().search(
                [('reward_year', '=', year)],
                order='reward_year desc, sequence_rewardee asc'
            )
        elif reward:
            rewardees = request.env['academy.rewardee'].sudo().search(
                [('reward_id', '=', reward.id)],
                order='reward_year desc, sequence_rewardee asc'
            )
        else:
            rewardees = request.env['academy.rewardee'].sudo().search(
                [],
                order='reward_year desc, sequence_rewardee asc'
            )

        return request.render(
            "website_academy_rewards.index_rewardees",
            {
                'reward': reward,
                'rewards': rewards,
                'rewardees': rewardees,
                'year': year
            }
        )



    @http.route(['/rewardee/<model("academy.rewardee"):rewardee>'], type='http', auth="public", website=True)
    def rewardee(self, page=0, year=0, rewardee=None, **post):
        rewards = request.env['academy.reward'].sudo().search([], order='sequence_reward')

        return request.render(
            "website_academy_rewards.index_rewardees",
            {
                'reward': rewardee.reward_id,
                'rewards': rewards,
                'rewardees': request.env['academy.rewardee'].sudo().browse(rewardee.id),
                'year': rewardee.reward_year
            }
        )


    @http.route(['/attachment/<model("ir.attachment"):attachment>/<string:file_name>'],
                type='http', auth="public", website=True)
    def get_attachment(self, attachment=None, file_name=None, **post):



                filecontent = attachment.raw or b""

                raw = attachment.res_name or attachment.name or attachment.datas_fname or "document"
                filename = str(raw).replace(" ", "_")

                mimetype = attachment.mimetype or "application/octet-stream"

                headers = [
                    ("Content-Type", mimetype),
                    ("Content-Disposition", f'inline; filename="{filename}"'),
                    ("Content-Length", str(len(filecontent))),
                ]

                return request.make_response(filecontent, headers=headers)


