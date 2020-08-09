# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import csv
import inspect
import os

import io
import base64
from werkzeug.datastructures import FileStorage
import tempfile
from gcloud import storage
from datetime import datetime as dt


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

        self.send_csv_google_cloud('/tmp/google_cloud/csv')  # <-- PASA AQUI LA DIRECCION DEL ARCHIVO CSV EN LA CARPETA DONDE LO TIRASTE Y YA

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

    def send_csv_google_cloud(self, file_path):
        company_id = self.env['res.company'].search([], limit=1)
        bucket = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.bucket', False)

        if not bucket:
            self.env['cron.log'].create({
                'log': 'No existe un bucket definido en las configuraciones.',
                'type': 'Error',
            })
            return 0

        if not company_id.credentials_json:
            self.env['cron.log'].create({
                'log': 'No existe un fichero json con credenciales definido.',
                'type': 'Error',
            })
            return 0

        try:
            # Leer el json y guardarlo en TEMP
            with io.BytesIO(base64.b64decode(company_id.credentials_json)) as fp:
                file = FileStorage(fp)
                with tempfile.NamedTemporaryFile(delete=False) as data_file:
                    file.save(data_file)

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = data_file.name  # Set gloud credentials.
            client = storage.Client()  # Set gcloud client.
            bucket = client.get_bucket(bucket)  # Specify gcloud bucket.
            blob = bucket.blob("reporte-%s.csv" % dt.now().strftime('%Y-%m-%d %H:%M:%S'))
            blob.upload_from_filename(file_path)

            self.env['cron.log'].create({
                'log': 'Reporte subido con exito.',
                'type': 'Info',
            })

            make_file_public = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.make_file_public', False)
            if make_file_public:
                blob.make_public()
                url = blob.public_url
                self.env['cron.log'].create({
                    'log': 'Publicando fichero en URL: %s' % url,
                    'type': 'Info',
                })
        except Exception as e:
            self.env['cron.log'].create({
                'log': 'ERROR enviando fichero: %s' % str(e),
                'type': 'Error',
            })

