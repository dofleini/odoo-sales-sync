# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import csv
import inspect
import os


class OrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def send_resume(self):
        directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        csv_path = os.path.join(directory_path, 'tabla.csv')

        file = open(csv_path, 'w')

        orders_lines = self.env['sale.order.line'].search([])

        with file:

            writer = csv.DictWriter(file, fieldnames=self.csv_header())
            writer.writeheader()

            for line in orders_lines:
                writer.writerow(self.csv_line(line))
        print("csv wrote")

    def csv_header(self):
        header = []

        line_id = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_id', False)
        if line_id:
            header += 'id'

        return header

    def csv_line(self, line):

        vals = {}

        line_id = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_id', False)
        if line_id and line.id:
            vals['id'] = line.id
        elif line_id and not line.id:
            vals['id'] = ''

        return vals


