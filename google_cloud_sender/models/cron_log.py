# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class CronLog(models.Model):
    _name = 'cron.log'
    _description = 'Logs del Cron'

    log = fields.Char('Log')
    type = fields.Char('Tipo', default='Info')


