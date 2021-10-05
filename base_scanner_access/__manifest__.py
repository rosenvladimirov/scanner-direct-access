# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Dicrect access to scanner",
    'version': '11.0.1.0.0',
    'category': 'Generic Modules/Base',
    "author": "Rosen Vladimirov <vladimirov.rosen@gmail.com>, "
              "dXFactory Ltd. <http://www.dxfactory.eu>",
    'license': 'AGPL-3',
    "depends": ['web', 'base'],
    'data': [
        'security/base_scanner_access.xml',
        'security/ir.model.access.csv',
        'views/scanning_scenner.xml',
        'views/res_users.xml',
        'wizards/scanning_scanner_update_wizard.xml',
    ],
    'installable': True,
    'application': False,
    'external_dependencies': {
        'python': ['sane'],
    },
}
