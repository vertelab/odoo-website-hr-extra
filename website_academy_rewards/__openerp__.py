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

{
    'name': 'Academy Awards',
    'category': 'Website',
    'website': 'https://www.vertel.se',
    'summary': 'Academy rewards with partners as rewardees',
    'version': '1.0',
    'description': """
Acacemy Rewards
===========================
""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'depends': [
        'website',
        'website_google_map',
        'website_imagemagick',
        'website_blog',
    ],
    'data': [
        'views/website_academy_rewards.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [],
    'installable': True,
}
