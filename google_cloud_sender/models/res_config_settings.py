# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # linea de productos
    line_id = fields.Boolean(config_parameter='google_cloud_sender.line_id', default='True')
    line_last_update = fields.Boolean(config_parameter='google_cloud_sender.line_last_update', default='True')
    line_company_id = fields.Boolean(config_parameter='google_cloud_sender.line_company_id', default='True')
    line_create_date = fields.Boolean(config_parameter='google_cloud_sender.line_create_date', default='True')
    line_create_uid = fields.Boolean(config_parameter='google_cloud_sender.line_create_uid', default='True')
    line_currency_id = fields.Boolean(config_parameter='google_cloud_sender.line_currency_id', default='True')
    line_customer_lead = fields.Boolean(config_parameter='google_cloud_sender.line_customer_lead', default='True')
    line_discount = fields.Boolean(config_parameter='google_cloud_sender.line_discount', default='True')
    line_display_name = fields.Boolean(config_parameter='google_cloud_sender.line_display_name', default='True')
    line_display_type = fields.Boolean(config_parameter='google_cloud_sender.line_display_type', default='True')
    line_invoice_status = fields.Boolean(config_parameter='google_cloud_sender.line_invoice_status', default='True')
    line_is_downpayment = fields.Boolean(config_parameter='google_cloud_sender.line_is_downpayment', default='True')
    line_is_expense = fields.Boolean(config_parameter='google_cloud_sender.line_is_expense', default='True')
    line_name = fields.Boolean(config_parameter='google_cloud_sender.line_name', default='True')
    line_name_short = fields.Boolean(config_parameter='google_cloud_sender.line_name_short', default='True')
    line_price_reduce = fields.Boolean(config_parameter='google_cloud_sender.line_price_reduce', default='True')
    line_price_reduce_taxexcl = fields.Boolean(config_parameter='google_cloud_sender.line_price_reduce_taxexcl',
                                               default='True')
    line_price_reduce_taxinc = fields.Boolean(config_parameter='google_cloud_sender.line_price_reduce_taxinc',
                                              default='True')
    line_price_subtotal = fields.Boolean(config_parameter='google_cloud_sender.line_price_subtotal', default='True')
    line_price_tax = fields.Boolean(config_parameter='google_cloud_sender.line_price_tax', default='True')
    line_price_total = fields.Boolean(config_parameter='google_cloud_sender.line_price_total', default='True')
    line_price_unit = fields.Boolean(config_parameter='google_cloud_sender.line_price_unit', default='True')
    line_product_uom = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom', default='True')
    line_product_uom_category_id = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom_category_id',
                                                  default='True')
    line_product_uom_qty = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom_qty', default='True')
    line_product_updatable = fields.Boolean(config_parameter='google_cloud_sender.line_product_updatable',
                                            default='True')
    line_qty_delivered = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered', default='True')
    line_qty_delivered_manual = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered_manual',
                                               default='True')
    line_qty_delivered_method = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered_method',
                                               default='True')

    order_id = fields.Boolean(config_parameter='google_cloud_sender.order_id', default='True')
    name = fields.Boolean(config_parameter='google_cloud_sender.name', default='True')

    credentials_json = fields.Binary('Credenciales OAuth Json', related='company_id.credentials_json', readonly=False)
    make_file_public = fields.Boolean(string="Hacer el fichero público", config_parameter='google_cloud_sender.make_file_public')
    bucket = fields.Char(string="Bucket", config_parameter='google_cloud_sender.bucket')

