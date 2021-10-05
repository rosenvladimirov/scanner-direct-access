# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import tempfile
import sane
import logging
import os
import io
import base64

from odoo import models, fields, api, _
#from odoo.tools.image import image_save_for_web
#from contextlib import closing
from odoo.exceptions import UserError, AccessError

_logger = logging.getLogger(__name__)

class ScannerAction(models.Model):
    _name = 'scanners.action'
    _description = 'Scanners Job Action'

    @api.model
    def _available_action_types(self):
        return [
            ('server', 'Scan for Save'),
            ('client', 'Scan and Send to Client'),
            ('user_default', "Use user's defaults"),
        ]

    name = fields.Char(required=True)
    action_type = fields.Selection(
        selection=_available_action_types,
        string='Type',
        required=True,
        oldname='type'
    )

    def scan_image(self, res, scanning_scanner_id=False,
                   scanner_depth=False, scanner_color_mode=False, scanner_source_mode=False, scanner_paper_mode=False,
                   attachment_name=False):
        if not scanning_scanner_id:
            scanning_scanner_id = self.env.user.scanning_scanner_id
        if scanner_depth:
            scanner_depth = self.env.user.scanner_depth
        if scanner_color_mode:
            scanner_color_mode = self.env.user.scanner_color_mode
        if scanner_source_mode:
            scanner_source_mode = self.env.user.scanner_source_mode
        if scanner_paper_mode:
            scanner_paper_mode = self.env.user.scanner_paper_mode

        ver = sane.init()
        _logger.info("Sane version %s.%s.%s.%s" % ver[:4])
        devices = sane.get_devices()
        if scanning_scanner_id and scanning_scanner_id.device in [x[0] for x in devices]:
            device = scanning_scanner_id.device
        else:
            return
        dev = sane.open(device)
        params = dev.get_parameters()
        try:
            dev.resolution = int(scanner_depth)
        except:
            _logger.info('Cannot set depth, defaulting to %d' % params[3])
        else:
            _logger.info('Set the resolution=%s' % dev.resolution)
        try:
            dev.mode = scanner_color_mode
        except:
            _logger.info('Cannot set mode, defaulting to %s' % params[0])
        try:
            dev.source = scanner_source_mode
        except:
            _logger.info('Cannot set source, defaulting to %s' % params[0])

        prefix = 'ScanImage-'
        if not attachment_name:
            body_file_fd, attachment_name = tempfile.mkstemp(suffix='.pdf', prefix=prefix)
            os.remove(attachment_name)
            attachment_name = os.path.basename(attachment_name)
        stream = io.BytesIO()
        dev.start()
        im = dev.snap()
        _logger.info("Sane start to save %s" % attachment_name)
        im.save(stream, "PDF", save_all=True, append_images=[im.convert("RGB")])
        attachment_vals = {
            'datas': base64.encodebytes(stream.getvalue()),
            'datas_fname': attachment_name,
        }
        dev.close()
        attachment = None
        try:
            attachment = res.update(attachment_vals)
        except AccessError:
            _logger.info("Cannot save PDF report %r as attachment", attachment_name)
        else:
            _logger.info('The PDF document %s is now upload in the field', attachment_name)
        return attachment
