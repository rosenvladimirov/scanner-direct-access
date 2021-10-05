# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import models, api


_logger = logging.getLogger(__name__)


class ScanningScannerUpdateWizard(models.TransientModel):
    _name = 'scanning.scanner.update.wizard'
    _description = 'Scanning Scanner Update Wizard'

    @api.multi
    def action_ok(self):
        self.env['scanners.scanner'].action_update_scanners()

        return {
            'name': 'Scanners',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'scanners.scanner',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
