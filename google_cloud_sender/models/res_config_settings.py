# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    order_id = fields.Boolean(string="Orden ID", config_parameter='google_cloud_sender.order_id')
    name = fields.Boolean(string="Orden ID", config_parameter='google_cloud_sender.name')
