# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # No usar, comentariado en el XML
    cron_repeat_min = fields.Integer(
        string="Intervalo de actualización",
        config_parameter='google_cloud_sender.cron_repeat_min',
        help="Intervalo de tiempo definido para enviar la información hacia Google Cloud. Este tiempo está expresado "
             "en minutos. "
    )

    # No usar, comentariado en el XML
    order_id = fields.Boolean(string="Orden ID", config_parameter='google_cloud_sender.order_id')
    name = fields.Boolean(string="Orden ID", config_parameter='google_cloud_sender.name')
