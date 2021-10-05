# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import errno
import logging
import os
import sane
from tempfile import mkstemp

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

try:
    import sane
except ImportError:
    _logger.debug('Cannot `import sane`.')


class ScannersScanner(models.Model):
    """
    Scanners
    """

    _name = 'scanners.scanner'
    _description = 'Scanners'
    _order = 'name'

    name = fields.Char(required=True, index=True)
    vendor = fields.Char("Vendor")
    model = fields.Char("Model")
    description = fields.Text("Decription")
    device = fields.Char(required=True)
    version = fields.Text("Version")

    def _get_scaners(self):
        ver = sane.init()
        devices = sane.get_devices()
        if devices:
            for scanner in devices:
                dev = self.search([('device', '=', scanner[0])])
                if dev:
                    dev.device, dev.vendor, dev.model, dev.description = scanner
                else:
                    dev.create({'name': ("%s %s %s" % scanner[1:]).strip(),
                                'device': scanner[0],
                                'vendor': scanner[1],
                                'model': scanner[2],
                                'description': scanner[3],
                                'version': ver,
                                })

    @api.multi
    def action_update_scanners(self):
        return self._get_scaners()

    @api.multi
    def scan_image(self, res, target, attachment_name):
        attachment = res
        for record in self:
            attachment |= self.env['scanners.action'].scan_image(record, res, target, attachment_name)
        return attachment
