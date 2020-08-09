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
        orders_lines = self.env['sale.order.line'].search([])

        if not os.path.exists('/tmp/google_cloud'):
            os.mkdir('/tmp/google_cloud')

        with open('/tmp/google_cloud/data.csv', 'w') as file:
            writer = csv.DictWriter(file, fieldnames=self.csv_header())
            writer.writeheader()

            for line in orders_lines:
                writer.writerow(self.csv_line(line))

        print("csv wrote")
        # self.send_csv_google_cloud('/tmp/google_cloud/data.csv')

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

            make_file_public = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.make_file_public',
                                                                                False)
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

    def csv_header(self):
        header = []

        # Header del model sale.order.line
        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_id', False)
        if show_column:
            header.append('line_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_company_id', False)
        if show_column:
            header.append('line_company_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_create_date', False)
        if show_column:
            header.append('line_create_date')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_create_uid', False)
        if show_column:
            header.append('line_create_uid')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_currency_id', False)
        if show_column:
            header.append('line_currency_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_customer_lead', False)
        if show_column:
            header.append('line_customer_lead')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_discount', False)
        if show_column:
            header.append('line_discount')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_display_name', False)
        if show_column:
            header.append('line_display_name')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_display_type', False)
        if show_column:
            header.append('line_display_type')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_invoice_status', False)
        if show_column:
            header.append('line_invoice_status')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_is_downpayment', False)
        if show_column:
            header.append('line_is_downpayment')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_is_expense', False)
        if show_column:
            header.append('line_is_expense')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_name', False)
        if show_column:
            header.append('line_name')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_name_short', False)
        if show_column:
            header.append('line_name_short')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_reduce', False)
        if show_column:
            header.append('line_price_reduce')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_reduce_taxexcl',
                                                                       False)
        if show_column:
            header.append('line_price_reduce_taxexcl')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_reduce_taxinc',
                                                                       False)
        if show_column:
            header.append('line_price_reduce_taxinc')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_subtotal', False)
        if show_column:
            header.append('line_price_subtotal')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_tax', False)
        if show_column:
            header.append('line_price_tax')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_total', False)
        if show_column:
            header.append('line_price_total')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_unit', False)
        if show_column:
            header.append('line_price_unit')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_product_uom', False)
        if show_column:
            header.append('line_product_uom')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.line_product_uom_category_id', False)
        if show_column:
            header.append('line_product_uom_category_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_product_uom_qty',
                                                                       False)
        if show_column:
            header.append('line_product_uom_qty')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_product_updatable',
                                                                       False)
        if show_column:
            header.append('line_product_updatable')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_qty_delivered', False)
        if show_column:
            header.append('line_qty_delivered')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_qty_delivered_manual',
                                                                       False)
        if show_column:
            header.append('line_qty_delivered_manual')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_qty_delivered_method',
                                                                       False)
        if show_column:
            header.append('line_qty_delivered_method')

        # Header del model sale.order
        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_id', False)
        if show_column:
            header.append('order_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_access_token', False)
        if show_column:
            header.append('order_access_token')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_access_url', False)
        if show_column:
            header.append('order_access_url')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_access_warning',
                                                                       False)
        if show_column:
            header.append('order_access_warning')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.order_activity_date_deadline', False)
        if show_column:
            header.append('order_activity_date_deadline')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.order_activity_exception_decoration', False)
        if show_column:
            header.append('order_activity_exception_decoration')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.order_activity_exception_icon', False)
        if show_column:
            header.append('order_activity_exception_icon')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_ids', False)
        if show_column:
            header.append('order_activity_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_state',
                                                                       False)
        if show_column:
            header.append('order_activity_state')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_summary',
                                                                       False)
        if show_column:
            header.append('order_activity_summary')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_type_id',
                                                                       False)
        if show_column:
            header.append('order_activity_type_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_user_id',
                                                                       False)
        if show_column:
            header.append('order_activity_user_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_by_group',
                                                                       False)
        if show_column:
            header.append('order_amount_by_group')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_tax', False)
        if show_column:
            header.append('order_amount_tax')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_total', False)
        if show_column:
            header.append('order_amount_total')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_undiscounted',
                                                                       False)
        if show_column:
            header.append('order_amount_undiscounted')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_untaxed',
                                                                       False)
        if show_column:
            header.append('order_amount_untaxed')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_analytic_account_id',
                                                                       False)
        if show_column:
            header.append('order_analytic_account_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.order_authorized_transaction_ids', False)
        if show_column:
            header.append('order_authorized_transaction_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_campaign_id', False)
        if show_column:
            header.append('order_campaign_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_cart_quantity', False)
        if show_column:
            header.append('order_cart_quantity')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.order_cart_recovery_email_sent', False)
        if show_column:
            header.append('order_cart_recovery_email_sent')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_client_order_ref',
                                                                       False)
        if show_column:
            header.append('order_client_order_ref')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_commitment_date',
                                                                       False)
        if show_column:
            header.append('order_commitment_date')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_company_id', False)
        if show_column:
            header.append('order_company_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_create_date', False)
        if show_column:
            header.append('order_create_date')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_create_uid', False)
        if show_column:
            header.append('order_create_uid')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_currency_id', False)
        if show_column:
            header.append('order_currency_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_currency_rate', False)
        if show_column:
            header.append('order_currency_rate')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_date_order', False)
        if show_column:
            header.append('order_date_order')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_display_name', False)
        if show_column:
            header.append('order_display_name')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_expected_date', False)
        if show_column:
            header.append('order_expected_date')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_fiscal_position_id',
                                                                       False)
        if show_column:
            header.append('order_fiscal_position_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_invoice_count', False)
        if show_column:
            header.append('order_invoice_count')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_invoice_ids', False)
        if show_column:
            header.append('order_invoice_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_invoice_status',
                                                                       False)
        if show_column:
            header.append('order_invoice_status')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_is_abandoned_cart',
                                                                       False)
        if show_column:
            header.append('order_is_abandoned_cart')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_is_expired', False)
        if show_column:
            header.append('order_is_expired')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_medium_id', False)
        if show_column:
            header.append('order_medium_id')

        # Header del model product.product
        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_active', False)
        if show_column:
            header.append('product_active')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_activity_date_deadline', False)
        if show_column:
            header.append('product_activity_date_deadline')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_activity_exception_decoration', False)
        if show_column:
            header.append('product_activity_exception_decoration')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_activity_exception_icon', False)
        if show_column:
            header.append('product_activity_exception_icon')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_ids',
                                                                       False)
        if show_column:
            header.append('product_activity_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_state',
                                                                       False)
        if show_column:
            header.append('product_activity_state')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_summary',
                                                                       False)
        if show_column:
            header.append('product_activity_summary')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_type_id',
                                                                       False)
        if show_column:
            header.append('product_activity_type_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_user_id',
                                                                       False)
        if show_column:
            header.append('product_activity_user_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_alternative_product_ids', False)
        if show_column:
            header.append('product_alternative_product_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_attribute_line_ids',
                                                                       False)
        if show_column:
            header.append('product_attribute_line_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_barcode', False)
        if show_column:
            header.append('product_barcode')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_can_image_1024_be_zoomed', False)
        if show_column:
            header.append('product_can_image_1024_be_zoomed')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_can_image_variant_1024_be_zoomed', False)
        if show_column:
            header.append('product_can_image_variant_1024_be_zoomed')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_can_publish', False)
        if show_column:
            header.append('product_can_publish')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_categ_id', False)
        if show_column:
            header.append('product_categ_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_code', False)
        if show_column:
            header.append('product_code')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_color', False)
        if show_column:
            header.append('product_color')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_combination_indices', False)
        if show_column:
            header.append('product_combination_indices')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_company_id', False)
        if show_column:
            header.append('product_company_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_cost_currency_id',
                                                                       False)
        if show_column:
            header.append('product_cost_currency_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_create_date', False)
        if show_column:
            header.append('product_create_date')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_create_uid', False)
        if show_column:
            header.append('product_create_uid')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_currency_id', False)
        if show_column:
            header.append('product_currency_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_default_code',
                                                                       False)
        if show_column:
            header.append('product_default_code')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_description', False)
        if show_column:
            header.append('product_description')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_description_purchase', False)
        if show_column:
            header.append('product_description_purchase')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_description_sale',
                                                                       False)
        if show_column:
            header.append('product_description_sale')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_display_name',
                                                                       False)
        if show_column:
            header.append('product_display_name')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_expense_policy',
                                                                       False)
        if show_column:
            header.append('product_expense_policy')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_has_configurable_attributes', False)
        if show_column:
            header.append('product_has_configurable_attributes')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_id', False)
        if show_column:
            header.append('product_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_accessory_product_ids', False)
        if show_column:
            header.append('product_accessory_product_ids')

        # Header del model res.partner
        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_active', False)
        if show_column:
            header.append('client_active')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_active_lang_count',
                                                                       False)
        if show_column:
            header.append('client_active_lang_count')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.client_activity_date_deadline', False)
        if show_column:
            header.append('client_activity_date_deadline')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.client_activity_exception_decoration', False)
        if show_column:
            header.append('client_activity_exception_decoration')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.client_activity_exception_icon', False)
        if show_column:
            header.append('client_activity_exception_icon')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_ids', False)
        if show_column:
            header.append('client_activity_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_state',
                                                                       False)
        if show_column:
            header.append('client_activity_state')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_summary',
                                                                       False)
        if show_column:
            header.append('client_activity_summary')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_type_id',
                                                                       False)
        if show_column:
            header.append('client_activity_type_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_user_id',
                                                                       False)
        if show_column:
            header.append('client_activity_user_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_additional_info',
                                                                       False)
        if show_column:
            header.append('client_additional_info')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_bank_account_count',
                                                                       False)
        if show_column:
            header.append('client_bank_account_count')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_bank_ids', False)
        if show_column:
            header.append('client_bank_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_can_publish', False)
        if show_column:
            header.append('client_can_publish')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_category_id', False)
        if show_column:
            header.append('client_category_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_channel_ids', False)
        if show_column:
            header.append('client_channel_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_child_ids', False)
        if show_column:
            header.append('client_child_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_city', False)
        if show_column:
            header.append('client_city')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_color', False)
        if show_column:
            header.append('client_color')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_comment', False)
        if show_column:
            header.append('client_comment')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.client_commercial_company_name', False)
        if show_column:
            header.append('client_commercial_company_name')

        show_column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.client_commercial_partner_id', False)
        if show_column:
            header.append('client_commercial_partner_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_company_id', False)
        if show_column:
            header.append('client_company_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_company_name', False)
        if show_column:
            header.append('client_company_name')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_company_type', False)
        if show_column:
            header.append('client_company_type')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_contact_address',
                                                                       False)
        if show_column:
            header.append('client_contact_address')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_contract_ids', False)
        if show_column:
            header.append('client_contract_ids')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_country_id', False)
        if show_column:
            header.append('client_country_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_create_date', False)
        if show_column:
            header.append('client_create_date')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_create_uid', False)
        if show_column:
            header.append('client_create_uid')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_credit', False)
        if show_column:
            header.append('client_credit')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_credit_limit', False)
        if show_column:
            header.append('client_credit_limit')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_currency_id', False)
        if show_column:
            header.append('client_currency_id')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_customer_rank',
                                                                       False)
        if show_column:
            header.append('client_customer_rank')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_date', False)
        if show_column:
            header.append('client_date')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_debit', False)
        if show_column:
            header.append('client_debit')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_debit_limit', False)
        if show_column:
            header.append('client_debit_limit')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_display_name', False)
        if show_column:
            header.append('client_display_name')

        show_column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_email', False)
        if show_column:
            header.append('client_email')

        return header

    def csv_line(self, line):

        vals = {}

        # Columnas del model sale.order.line
        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_id', False)
        if column and line.id:
            vals['line_id'] = line.id
        elif column and not line.id:
            vals['line_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_company_id', False)
        if column and line.company_id:
            vals['line_company_id'] = line.company_id.id
        elif column and not line.company_id:
            vals['line_company_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_create_date', False)
        if column and line.create_date:
            vals['line_create_date'] = line.create_date
        elif column and not line.create_date:
            vals['line_create_date'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_create_uid', False)
        if column and line.create_uid:
            vals['line_create_uid'] = line.create_uid.id
        elif column and not line.create_uid:
            vals['line_create_uid'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_currency_id', False)
        if column and line.currency_id:
            vals['line_currency_id'] = line.currency_id.name
        elif column and not line.currency_id:
            vals['line_currency_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_customer_lead', False)
        if column and line.customer_lead:
            vals['line_customer_lead'] = line.customer_lead
        elif column and not line.customer_lead:
            vals['line_customer_lead'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_discount', False)
        if column and line.discount:
            vals['line_discount'] = line.discount
        elif column and not line.discount:
            vals['line_discount'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_display_name', False)
        if column and line.display_name:
            vals['line_display_name'] = line.display_name
        elif column and not line.display_name:
            vals['line_display_name'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_display_type', False)
        if column and line.display_type:
            vals['line_display_type'] = line.display_type
        elif column and not line.display_type:
            vals['line_display_type'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_invoice_status', False)
        if column and line.invoice_status:
            vals['line_invoice_status'] = line.invoice_status
        elif column and not line.invoice_status:
            vals['line_invoice_status'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_is_downpayment', False)
        if column and line.is_downpayment:
            vals['line_is_downpayment'] = line.is_downpayment
        elif column and not line.is_downpayment:
            vals['line_is_downpayment'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_is_expense', False)
        if column and line.is_expense:
            vals['line_is_expense'] = line.is_expense
        elif column and not line.is_expense:
            vals['line_is_expense'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_name', False)
        if column and line.name:
            vals['line_name'] = line.name
        elif column and not line.name:
            vals['line_name'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_name_short', False)
        if column and line.name_short:
            vals['line_name_short'] = line.name_short
        elif column and not line.name_short:
            vals['line_name_short'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_reduce', False)
        if column and line.price_reduce:
            vals['line_price_reduce'] = line.price_reduce
        elif column and not line.price_reduce:
            vals['line_price_reduce'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_reduce_taxexcl',
                                                                  False)
        if column and line.price_reduce_taxexcl:
            vals['line_price_reduce_taxexcl'] = line.price_reduce_taxexcl
        elif column and not line.price_reduce_taxexcl:
            vals['line_price_reduce_taxexcl'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_reduce_taxinc', False)
        if column and line.price_reduce_taxinc:
            vals['line_price_reduce_taxinc'] = line.price_reduce_taxinc
        elif column and not line.price_reduce_taxinc:
            vals['line_price_reduce_taxinc'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_subtotal', False)
        if column and line.price_subtotal:
            vals['line_price_subtotal'] = line.price_subtotal
        elif column and not line.price_subtotal:
            vals['line_price_subtotal'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_tax', False)
        if column and line.price_tax:
            vals['line_price_tax'] = line.price_tax
        elif column and not line.price_tax:
            vals['line_price_tax'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_total', False)
        if column and line.price_total:
            vals['line_price_total'] = line.price_total
        elif column and not line.price_total:
            vals['line_price_total'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_price_unit', False)
        if column and line.price_unit:
            vals['line_price_unit'] = line.price_unit
        elif column and not line.price_unit:
            vals['line_price_unit'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_product_uom', False)
        if column and line.product_uom:
            vals['line_product_uom'] = line.product_uom.id
        elif column and not line.product_uom:
            vals['line_product_uom'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_product_uom_category_id',
                                                                  False)
        if column and line.product_uom_category_id:
            vals['line_product_uom_category_id'] = line.product_uom_category_id.id
        elif column and not line.product_uom_category_id:
            vals['line_product_uom_category_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_product_uom_qty', False)
        if column and line.product_uom_qty:
            vals['line_product_uom_qty'] = line.product_uom_qty
        elif column and not line.product_uom_qty:
            vals['line_product_uom_qty'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_product_updatable', False)
        if column and line.product_updatable:
            vals['line_product_updatable'] = line.product_updatable
        elif column and not line.product_updatable:
            vals['line_product_updatable'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_qty_delivered', False)
        if column and line.qty_delivered:
            vals['line_qty_delivered'] = line.qty_delivered
        elif column and not line.qty_delivered:
            vals['line_qty_delivered'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_qty_delivered_manual',
                                                                  False)
        if column and line.qty_delivered_manual:
            vals['line_qty_delivered_manual'] = line.qty_delivered_manual
        elif column and not line.qty_delivered_manual:
            vals['line_qty_delivered_manual'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.line_qty_delivered_method',
                                                                  False)
        if column and line.qty_delivered_method:
            vals['line_qty_delivered_method'] = line.qty_delivered_method
        elif column and not line.qty_delivered_method:
            vals['line_qty_delivered_method'] = ''

        # Columnas del model sale.order
        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_id', False)
        if column and line.order_id.id:
            vals['order_id'] = line.order_id.id
        elif column and not line.order_id.id:
            vals['order_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_access_token', False)
        if column and line.order_id.access_token:
            vals['order_access_token'] = line.order_id.access_token
        elif column and not line.order_id.access_token:
            vals['order_access_token'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_access_url', False)
        if column and line.order_id.access_url:
            vals['order_access_url'] = line.order_id.access_url
        elif column and not line.order_id.access_url:
            vals['order_access_url'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_access_warning', False)
        if column and line.order_id.access_warning:
            vals['order_access_warning'] = line.order_id.access_warning
        elif column and not line.order_id.access_warning:
            vals['order_access_warning'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_date_deadline',
                                                                  False)
        if column and line.order_id.activity_date_deadline:
            vals['order_activity_date_deadline'] = line.order_id.activity_date_deadline
        elif column and not line.order_id.activity_date_deadline:
            vals['order_activity_date_deadline'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.order_activity_exception_decoration', False)
        if column and line.order_id.activity_exception_decoration:
            vals['order_activity_exception_decoration'] = line.order_id.activity_exception_decoration
        elif column and not line.order_id.activity_exception_decoration:
            vals['order_activity_exception_decoration'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_exception_icon',
                                                                  False)
        if column and line.order_id.activity_exception_icon:
            vals['order_activity_exception_icon'] = line.order_id.activity_exception_icon
        elif column and not line.order_id.activity_exception_icon:
            vals['order_activity_exception_icon'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_ids', False)
        if column and line.order_id.activity_ids:
            vals['order_activity_ids'] = line.order_id.activity_ids
        elif column and not line.order_id.activity_ids:
            vals['order_activity_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_state', False)
        if column and line.order_id.activity_state:
            vals['order_activity_state'] = line.order_id.activity_state
        elif column and not line.order_id.activity_state:
            vals['order_activity_state'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_summary', False)
        if column and line.order_id.activity_summary:
            vals['order_activity_summary'] = line.order_id.activity_summary
        elif column and not line.order_id.activity_summary:
            vals['order_activity_summary'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_type_id', False)
        if column and line.order_id.activity_type_id:
            vals['order_activity_type_id'] = line.order_id.activity_type_id
        elif column and not line.order_id.activity_type_id:
            vals['order_activity_type_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_activity_user_id', False)
        if column and line.order_id.activity_user_id:
            vals['order_activity_user_id'] = line.order_id.activity_user_id
        elif column and not line.order_id.activity_user_id:
            vals['order_activity_user_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_by_group', False)
        if column and line.order_id.amount_by_group:
            vals['order_amount_by_group'] = line.order_id.amount_by_group
        elif column and not line.order_id.amount_by_group:
            vals['order_amount_by_group'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_tax', False)
        if column and line.order_id.amount_tax:
            vals['order_amount_tax'] = line.order_id.amount_tax
        elif column and not line.order_id.amount_tax:
            vals['order_amount_tax'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_total', False)
        if column and line.order_id.amount_total:
            vals['order_amount_total'] = line.order_id.amount_total
        elif column and not line.order_id.amount_total:
            vals['order_amount_total'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_undiscounted',
                                                                  False)
        if column and line.order_id.amount_undiscounted:
            vals['order_amount_undiscounted'] = line.order_id.amount_undiscounted
        elif column and not line.order_id.amount_undiscounted:
            vals['order_amount_undiscounted'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_amount_untaxed', False)
        if column and line.order_id.amount_untaxed:
            vals['order_amount_untaxed'] = line.order_id.amount_untaxed
        elif column and not line.order_id.amount_untaxed:
            vals['order_amount_untaxed'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_analytic_account_id',
                                                                  False)
        if column and line.order_id.analytic_account_id:
            vals['order_analytic_account_id'] = line.order_id.analytic_account_id
        elif column and not line.order_id.analytic_account_id:
            vals['order_analytic_account_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.order_authorized_transaction_ids', False)
        if column and line.order_id.authorized_transaction_ids:
            vals['order_authorized_transaction_ids'] = line.order_id.authorized_transaction_ids
        elif column and not line.order_id.authorized_transaction_ids:
            vals['order_authorized_transaction_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_campaign_id', False)
        if column and line.order_id.campaign_id:
            vals['order_campaign_id'] = line.order_id.campaign_id
        elif column and not line.order_id.campaign_id:
            vals['order_campaign_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_cart_quantity', False)
        if column and line.order_id.cart_quantity:
            vals['order_cart_quantity'] = line.order_id.cart_quantity
        elif column and not line.order_id.cart_quantity:
            vals['order_cart_quantity'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_cart_recovery_email_sent',
                                                                  False)
        if column and line.order_id.cart_recovery_email_sent:
            vals['order_cart_recovery_email_sent'] = line.order_id.cart_recovery_email_sent
        elif column and not line.order_id.cart_recovery_email_sent:
            vals['order_cart_recovery_email_sent'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_client_order_ref', False)
        if column and line.order_id.client_order_ref:
            vals['order_client_order_ref'] = line.order_id.client_order_ref
        elif column and not line.order_id.client_order_ref:
            vals['order_client_order_ref'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_commitment_date', False)
        if column and line.order_id.commitment_date:
            vals['order_commitment_date'] = line.order_id.commitment_date
        elif column and not line.order_id.commitment_date:
            vals['order_commitment_date'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_company_id', False)
        if column and line.order_id.company_id:
            vals['order_company_id'] = line.order_id.company_id.id
        elif column and not line.order_id.company_id:
            vals['order_company_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_create_date', False)
        if column and line.order_id.create_date:
            vals['order_create_date'] = line.order_id.create_date
        elif column and not line.order_id.create_date:
            vals['order_create_date'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_create_uid', False)
        if column and line.order_id.create_uid:
            vals['order_create_uid'] = line.order_id.create_uid.id
        elif column and not line.order_id.create_uid:
            vals['order_create_uid'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_currency_id', False)
        if column and line.order_id.currency_id:
            vals['order_currency_id'] = line.order_id.currency_id.name
        elif column and not line.order_id.currency_id:
            vals['order_currency_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.order_currency_rate', False)
        if column and line.order_id.currency_rate:
            vals['order_currency_rate'] = line.order_id.currency_rate
        elif column and not line.order_id.currency_rate:
            vals['order_currency_rate'] = ''

        # Columnas del model product.product
        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_active', False)
        if column and line.product_id.active:
            vals['product_active'] = line.product_id.active
        elif column and not line.product_id.active:
            vals['product_active'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_date_deadline',
                                                                  False)
        if column and line.product_id.activity_date_deadline:
            vals['product_activity_date_deadline'] = line.product_id.activity_date_deadline
        elif column and not line.product_id.activity_date_deadline:
            vals['product_activity_date_deadline'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_activity_exception_decoration', False)
        if column and line.product_id.activity_exception_decoration:
            vals['product_activity_exception_decoration'] = line.product_id.activity_exception_decoration
        elif column and not line.product_id.activity_exception_decoration:
            vals['product_activity_exception_decoration'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_exception_icon',
                                                                  False)
        if column and line.product_id.activity_exception_icon:
            vals['product_activity_exception_icon'] = line.product_id.activity_exception_icon
        elif column and not line.product_id.activity_exception_icon:
            vals['product_activity_exception_icon'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_ids', False)
        if column and line.product_id.activity_ids:
            vals['product_activity_ids'] = line.product_id.activity_ids
        elif column and not line.product_id.activity_ids:
            vals['product_activity_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_state', False)
        if column and line.product_id.activity_state:
            vals['product_activity_state'] = line.product_id.activity_state
        elif column and not line.product_id.activity_state:
            vals['product_activity_state'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_summary', False)
        if column and line.product_id.activity_summary:
            vals['product_activity_summary'] = line.product_id.activity_summary
        elif column and not line.product_id.activity_summary:
            vals['product_activity_summary'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_type_id', False)
        if column and line.product_id.activity_type_id:
            vals['product_activity_type_id'] = line.product_id.activity_type_id
        elif column and not line.product_id.activity_type_id:
            vals['product_activity_type_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_activity_user_id', False)
        if column and line.product_id.activity_user_id:
            vals['product_activity_user_id'] = line.product_id.activity_user_id
        elif column and not line.product_id.activity_user_id:
            vals['product_activity_user_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_alternative_product_ids',
                                                                  False)
        if column and line.product_id.alternative_product_ids:
            vals['product_alternative_product_ids'] = line.product_id.alternative_product_ids
        elif column and not line.product_id.alternative_product_ids:
            vals['product_alternative_product_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_attribute_line_ids',
                                                                  False)
        if column and line.product_id.attribute_line_ids:
            vals['product_attribute_line_ids'] = line.product_id.attribute_line_ids
        elif column and not line.product_id.attribute_line_ids:
            vals['product_attribute_line_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_barcode', False)
        if column and line.product_id.barcode:
            vals['product_barcode'] = line.product_id.barcode
        elif column and not line.product_id.barcode:
            vals['product_barcode'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_can_image_1024_be_zoomed', False)
        if column and line.product_id.can_image_1024_be_zoomed:
            vals['product_can_image_1024_be_zoomed'] = line.product_id.can_image_1024_be_zoomed
        elif column and not line.product_id.can_image_1024_be_zoomed:
            vals['product_can_image_1024_be_zoomed'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_can_image_variant_1024_be_zoomed', False)
        if column and line.product_id.can_image_variant_1024_be_zoomed:
            vals['product_can_image_variant_1024_be_zoomed'] = line.product_id.can_image_variant_1024_be_zoomed
        elif column and not line.product_id.can_image_variant_1024_be_zoomed:
            vals['product_can_image_variant_1024_be_zoomed'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_can_publish', False)
        if column and line.product_id.can_publish:
            vals['product_can_publish'] = line.product_id.can_publish
        elif column and not line.product_id.can_publish:
            vals['product_can_publish'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_categ_id', False)
        if column and line.product_id.categ_id:
            vals['product_categ_id'] = line.product_id.categ_id.id
        elif column and not line.product_id.categ_id:
            vals['product_categ_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_code', False)
        if column and line.product_id.code:
            vals['product_code'] = line.product_id.code
        elif column and not line.product_id.code:
            vals['product_code'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_color', False)
        if column and line.product_id.color:
            vals['product_color'] = line.product_id.color
        elif column and not line.product_id.color:
            vals['product_color'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_combination_indices',
                                                                  False)
        if column and line.product_id.combination_indices:
            vals['product_combination_indices'] = line.product_id.combination_indices
        elif column and not line.product_id.combination_indices:
            vals['product_combination_indices'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_company_id', False)
        if column and line.product_id.company_id:
            vals['product_company_id'] = line.product_id.company_id.id
        elif column and not line.product_id.company_id:
            vals['product_company_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_cost_currency_id', False)
        if column and line.product_id.cost_currency_id:
            vals['product_cost_currency_id'] = line.product_id.cost_currency_id.id
        elif column and not line.product_id.cost_currency_id:
            vals['product_cost_currency_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_create_date', False)
        if column and line.product_id.create_date:
            vals['product_create_date'] = line.product_id.create_date
        elif column and not line.product_id.create_date:
            vals['product_create_date'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_create_uid', False)
        if column and line.product_id.create_uid:
            vals['product_create_uid'] = line.product_id.create_uid.id
        elif column and not line.product_id.create_uid:
            vals['product_create_uid'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_currency_id', False)
        if column and line.product_id.currency_id:
            vals['product_currency_id'] = line.product_id.currency_id.name
        elif column and not line.product_id.currency_id:
            vals['product_currency_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_default_code', False)
        if column and line.product_id.default_code:
            vals['product_default_code'] = line.product_id.default_code
        elif column and not line.product_id.default_code:
            vals['product_default_code'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_description', False)
        if column and line.product_id.description:
            vals['product_description'] = line.product_id.description
        elif column and not line.product_id.description:
            vals['product_description'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_description_purchase',
                                                                  False)
        if column and line.product_id.description_purchase:
            vals['product_description_purchase'] = line.product_id.description_purchase
        elif column and not line.product_id.description_purchase:
            vals['product_description_purchase'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_description_sale', False)
        if column and line.product_id.description_sale:
            vals['product_description_sale'] = line.product_id.description_sale
        elif column and not line.product_id.description_sale:
            vals['product_description_sale'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_display_name', False)
        if column and line.product_id.display_name:
            vals['product_display_name'] = line.product_id.display_name
        elif column and not line.product_id.display_name:
            vals['product_display_name'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_expense_policy', False)
        if column and line.product_id.expense_policy:
            vals['product_expense_policy'] = line.product_id.expense_policy
        elif column and not line.product_id.expense_policy:
            vals['product_expense_policy'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.product_has_configurable_attributes', False)
        if column and line.product_id.has_configurable_attributes:
            vals['product_has_configurable_attributes'] = line.product_id.has_configurable_attributes
        elif column and not line.product_id.has_configurable_attributes:
            vals['product_has_configurable_attributes'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_id', False)
        if column and line.product_id.id:
            vals['product_id'] = line.product_id.id
        elif column and not line.product_id.id:
            vals['product_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.product_accessory_product_ids',
                                                                  False)
        if column and line.product_id.accessory_product_ids:
            vals['product_accessory_product_ids'] = line.product_id.accessory_product_ids
        elif column and not line.product_id.accessory_product_ids:
            vals['product_accessory_product_ids'] = ''

        # Columnas del model sale.order.line
        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_active', False)
        if column and line.order_partner_id.active:
            vals['client_active'] = line.order_partner_id.active
        elif column and not line.order_partner_id.active:
            vals['client_active'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_active_lang_count', False)
        if column and line.order_partner_id.active_lang_count:
            vals['client_active_lang_count'] = line.order_partner_id.active_lang_count
        elif column and not line.order_partner_id.active_lang_count:
            vals['client_active_lang_count'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_date_deadline',
                                                                  False)
        if column and line.order_partner_id.activity_date_deadline:
            vals['client_activity_date_deadline'] = line.order_partner_id.activity_date_deadline
        elif column and not line.order_partner_id.activity_date_deadline:
            vals['client_activity_date_deadline'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param(
            'google_cloud_sender.client_activity_exception_decoration', False)
        if column and line.order_partner_id.activity_exception_decoration:
            vals['client_activity_exception_decoration'] = line.order_partner_id.activity_exception_decoration
        elif column and not line.order_partner_id.activity_exception_decoration:
            vals['client_activity_exception_decoration'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_exception_icon',
                                                                  False)
        if column and line.order_partner_id.activity_exception_icon:
            vals['client_activity_exception_icon'] = line.order_partner_id.activity_exception_icon
        elif column and not line.order_partner_id.activity_exception_icon:
            vals['client_activity_exception_icon'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_ids', False)
        if column and line.order_partner_id.activity_ids:
            vals['client_activity_ids'] = line.order_partner_id.activity_ids
        elif column and not line.order_partner_id.activity_ids:
            vals['client_activity_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_state', False)
        if column and line.order_partner_id.activity_state:
            vals['client_activity_state'] = line.order_partner_id.activity_state
        elif column and not line.order_partner_id.activity_state:
            vals['client_activity_state'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_summary', False)
        if column and line.order_partner_id.activity_summary:
            vals['client_activity_summary'] = line.order_partner_id.activity_summary
        elif column and not line.order_partner_id.activity_summary:
            vals['client_activity_summary'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_type_id', False)
        if column and line.order_partner_id.activity_type_id:
            vals['client_activity_type_id'] = line.order_partner_id.activity_type_id.id
        elif column and not line.order_partner_id.activity_type_id:
            vals['client_activity_type_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_activity_user_id', False)
        if column and line.order_partner_id.activity_user_id:
            vals['client_activity_user_id'] = line.order_partner_id.activity_user_id.id
        elif column and not line.order_partner_id.activity_user_id:
            vals['client_activity_user_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_additional_info', False)
        if column and line.order_partner_id.additional_info:
            vals['client_additional_info'] = line.order_partner_id.additional_info
        elif column and not line.order_partner_id.additional_info:
            vals['client_additional_info'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_bank_account_count',
                                                                  False)
        if column and line.order_partner_id.bank_account_count:
            vals['client_bank_account_count'] = line.order_partner_id.bank_account_count
        elif column and not line.order_partner_id.bank_account_count:
            vals['client_bank_account_count'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_bank_ids', False)
        if column and line.order_partner_id.bank_ids:
            vals['client_bank_ids'] = line.order_partner_id.bank_ids
        elif column and not line.order_partner_id.bank_ids:
            vals['client_bank_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_can_publish', False)
        if column and line.order_partner_id.can_publish:
            vals['client_can_publish'] = line.order_partner_id.can_publish
        elif column and not line.order_partner_id.can_publish:
            vals['client_can_publish'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_category_id', False)
        if column and line.order_partner_id.category_id:
            vals['client_category_id'] = line.order_partner_id.category_id
        elif column and not line.order_partner_id.category_id:
            vals['client_category_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_channel_ids', False)
        if column and line.order_partner_id.channel_ids:
            vals['client_channel_ids'] = line.order_partner_id.channel_ids
        elif column and not line.order_partner_id.channel_ids:
            vals['client_channel_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_child_ids', False)
        if column and line.order_partner_id.child_ids:
            vals['client_child_ids'] = line.order_partner_id.child_ids
        elif column and not line.order_partner_id.child_ids:
            vals['client_child_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_city', False)
        if column and line.order_partner_id.city:
            vals['client_city'] = line.order_partner_id.city
        elif column and not line.order_partner_id.city:
            vals['client_city'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_color', False)
        if column and line.order_partner_id.color:
            vals['client_color'] = line.order_partner_id.color
        elif column and not line.order_partner_id.color:
            vals['client_color'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_comment', False)
        if column and line.order_partner_id.comment:
            vals['client_comment'] = line.order_partner_id.comment
        elif column and not line.order_partner_id.comment:
            vals['client_comment'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_commercial_company_name',
                                                                  False)
        if column and line.order_partner_id.commercial_company_name:
            vals['client_commercial_company_name'] = line.order_partner_id.commercial_company_name
        elif column and not line.order_partner_id.commercial_company_name:
            vals['client_commercial_company_name'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_commercial_partner_id',
                                                                  False)
        if column and line.order_partner_id.commercial_partner_id:
            vals['client_commercial_partner_id'] = line.order_partner_id.commercial_partner_id.id
        elif column and not line.order_partner_id.commercial_partner_id:
            vals['client_commercial_partner_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_company_id', False)
        if column and line.order_partner_id.company_id:
            vals['client_company_id'] = line.order_partner_id.company_id.id
        elif column and not line.order_partner_id.company_id:
            vals['client_company_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_company_name', False)
        if column and line.order_partner_id.company_name:
            vals['client_company_name'] = line.order_partner_id.company_name
        elif column and not line.order_partner_id.company_name:
            vals['client_company_name'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_company_type', False)
        if column and line.order_partner_id.company_type:
            vals['client_company_type'] = line.order_partner_id.company_type
        elif column and not line.order_partner_id.company_type:
            vals['client_company_type'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_contact_address', False)
        if column and line.order_partner_id.contact_address:
            vals['client_contact_address'] = line.order_partner_id.contact_address
        elif column and not line.order_partner_id.contact_address:
            vals['client_contact_address'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_contract_ids', False)
        if column and line.order_partner_id.contract_ids:
            vals['client_contract_ids'] = line.order_partner_id.contract_ids
        elif column and not line.order_partner_id.contract_ids:
            vals['client_contract_ids'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_country_id', False)
        if column and line.order_partner_id.country_id:
            vals['client_country_id'] = line.order_partner_id.country_id.name
        elif column and not line.order_partner_id.country_id:
            vals['client_country_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_create_date', False)
        if column and line.order_partner_id.create_date:
            vals['client_create_date'] = line.order_partner_id.create_date
        elif column and not line.order_partner_id.create_date:
            vals['client_create_date'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_create_uid', False)
        if column and line.order_partner_id.create_uid:
            vals['client_create_uid'] = line.order_partner_id.create_uid.id
        elif column and not line.order_partner_id.create_uid:
            vals['client_create_uid'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_credit', False)
        if column and line.order_partner_id.credit:
            vals['client_credit'] = line.order_partner_id.credit
        elif column and not line.order_partner_id.credit:
            vals['client_credit'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_credit_limit', False)
        if column and line.order_partner_id.credit_limit:
            vals['client_credit_limit'] = line.order_partner_id.credit_limit
        elif column and not line.order_partner_id.credit_limit:
            vals['client_credit_limit'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_currency_id', False)
        if column and line.order_partner_id.currency_id:
            vals['client_currency_id'] = line.order_partner_id.currency_id.id
        elif column and not line.order_partner_id.currency_id:
            vals['client_currency_id'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_customer_rank', False)
        if column and line.order_partner_id.customer_rank:
            vals['client_customer_rank'] = line.order_partner_id.customer_rank
        elif column and not line.order_partner_id.customer_rank:
            vals['client_customer_rank'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_date', False)
        if column and line.order_partner_id.date:
            vals['client_date'] = line.order_partner_id.date
        elif column and not line.order_partner_id.date:
            vals['client_date'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_debit', False)
        if column and line.order_partner_id.debit:
            vals['client_debit'] = line.order_partner_id.debit
        elif column and not line.order_partner_id.debit:
            vals['client_debit'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_debit_limit', False)
        if column and line.order_partner_id.debit_limit:
            vals['client_debit_limit'] = line.order_partner_id.debit_limit
        elif column and not line.order_partner_id.debit_limit:
            vals['client_debit_limit'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_display_name', False)
        if column and line.order_partner_id.display_name:
            vals['client_display_name'] = line.order_partner_id.display_name
        elif column and not line.order_partner_id.display_name:
            vals['client_display_name'] = ''

        column = self.env['ir.config_parameter'].sudo().get_param('google_cloud_sender.client_email', False)
        if column and line.order_partner_id.email:
            vals['client_email'] = line.order_partner_id.email
        elif column and not line.order_partner_id.email:
            vals['client_email'] = ''

        return vals
