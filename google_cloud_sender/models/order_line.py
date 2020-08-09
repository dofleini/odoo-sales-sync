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

            f_names = ['product_id', 'product_uom_qty']
            writer = csv.DictWriter(file, fieldnames=f_names)
            writer.writeheader()

            for line in orders_lines:
                writer.writerow(self.csv_line(line))

    @staticmethod
    def csv_line(line):

        vals = {}

        if line.product_id:
            vals['product_id'] = line.product_id.name
        else:
            vals['product_id'] = ''

        if line.product_uom_qty:
            vals['product_uom_qty'] = line.product_uom_qty
        else:
            vals['product_uom_qty'] = ''

        return vals


