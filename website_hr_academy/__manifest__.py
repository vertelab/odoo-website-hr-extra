# -*- coding: utf-8 -*-
##############################################################################
#
#
#
##############################################################################


{
    'name': 'HR Academy',
    'version': '18.0.1.1.0',
    'category': 'Human Resources',
    'summary': 'Employees viewed as a academy.',
    'description': '''
HR Academy
==========

    Employees viewed as a academy.

    Features:

        - UI Integration: Extends 1 view(s) in the Odoo interface.
        - Extends Odoo: Builds on hr.employee.
    ''',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'https://vertel.se/apps/odoo-website-hr-extra/website_hr_academy',
    'depends': [
                'website',
                'hr',
                #'website_hr',
                'website_imagemagick'
               ],
    'data': ['views/website_hr_view.xml',
             'data/website_hr_data.xml'
             ],

    'installable': True,
    #'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
