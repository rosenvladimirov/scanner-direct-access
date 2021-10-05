# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _user_available_action_types(self):
        return [
            (code, string)
            for code, string
            in self.env['printing.action']._available_action_types()
            if code != 'user_default'
        ]

    scanning_action = fields.Selection(
        selection=_user_available_action_types,
    )
    scanning_scanner_id = fields.Many2one(comodel_name='scanners.scanner', string='Default Scanner')

    scanner_depth = fields.Selection([
        ('50', '50 dpi'),
        ('100', '100 dpi'),
        ('150', '150 dpi'),
        ('200', '200 dpi'),
        ('300', '300 dpi'),
        ('400', '400 dpi'),
        ('600', '600 dpi'),
        ('1200', '1200 dpi')
        ], string='Resolution', default='100')

    scanner_color_mode = fields.Selection([
        ('Color', 'Color'),
        ('Monochrome', 'Monochrome'),
        ('Grayscale', 'Grayscale'),
        ], string='Mode', default='mono')

    scanner_source_mode = fields.Selection([
        ('ADF', 'ADF'),
        ('Document Table', 'Document Table'),
        ], string='Document Source', default='adf')

    scanner_paper_mode = fields.Selection([
        ('Executive/Portrait', 'Executive/Portrait'),
        ('ISO/A4/Portrait', 'ISO/A4/Portrait'),
        ('ISO/A5/Portrait', 'ISO/A5/Portrait'),
        ('ISO/A5/Landscape', 'ISO/A5/Landscape'),
        ('ISO/A6/Portrait', 'ISO/A6/Portrait'),
        ('ISO/A6/Landscape', 'ISO/A6/Landscape'),
        ('JIS/B5/Portrait', 'JIS/B5/Portrait'),
        ('JIS/B6/Portrait', 'JIS/B6/Portrait'),
        ('JIS/B6/Landscape', 'JIS/B6/Landscape'),
        ('Letter/Portrait', 'Letter/Portrait'),
        ('Manual', 'Manual'),
        ('Maximum', 'Maximum'),
        ], string='Scan Area', default='a4portrait')


    @api.model
    def _register_hook(self):
        self.SELF_WRITEABLE_FIELDS.extend([
            'scanning_action',
            'scanning_scanner_id',
        ])
        self.SELF_READABLE_FIELDS.extend([
            'scanning_action',
            'scanning_scanner_id',
        ])
