# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import csv
import inspect
import os


class Company(models.Model):
    _inherit = 'res.company'

    credentials_json = fields.Binary('Credenciales OAuth Json')
