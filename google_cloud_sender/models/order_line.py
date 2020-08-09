# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class OrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def send_resume(self):
        print('message from cron')

