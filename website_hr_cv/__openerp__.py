# -*- coding: utf-8 -*-
##############################################################################
#
#
#
##############################################################################


{
    'name': 'HR CV-database',
    'version': '1.0',
    'category': 'other',
    'summary': 'Employees viewed as consultants',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['website_hr_recruitment', 'website_imagemagick', 'crm'],
    'data': ['website_hr.xml', 'website_hr_data.xml', 'security/ir.model.access.csv'],

    'installable': True,
    'application': False,
    #'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
