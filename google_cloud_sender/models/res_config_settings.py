# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # linea de productos
    line_id = fields.Boolean(config_parameter='google_cloud_sender.line_id')
    line_last_update = fields.Boolean(config_parameter='google_cloud_sender.line_last_update')
    line_company_id = fields.Boolean(config_parameter='google_cloud_sender.line_company_id')
    line_create_date = fields.Boolean(config_parameter='google_cloud_sender.line_create_date')
    line_create_uid = fields.Boolean(config_parameter='google_cloud_sender.line_create_uid')
    line_currency_id = fields.Boolean(config_parameter='google_cloud_sender.line_currency_id')
    line_customer_lead = fields.Boolean(config_parameter='google_cloud_sender.line_customer_lead')
    line_discount = fields.Boolean(config_parameter='google_cloud_sender.line_discount')
    line_display_name = fields.Boolean(config_parameter='google_cloud_sender.line_display_name')
    line_display_type = fields.Boolean(config_parameter='google_cloud_sender.line_display_type')
    line_invoice_status = fields.Boolean(config_parameter='google_cloud_sender.line_invoice_status')
    line_is_downpayment = fields.Boolean(config_parameter='google_cloud_sender.line_is_downpayment')
    line_is_expense = fields.Boolean(config_parameter='google_cloud_sender.line_is_expense')
    line_name = fields.Boolean(config_parameter='google_cloud_sender.line_name')
    line_name_short = fields.Boolean(config_parameter='google_cloud_sender.line_name_short')
    line_price_reduce = fields.Boolean(config_parameter='google_cloud_sender.line_price_reduce')
    line_price_reduce_taxexcl = fields.Boolean(config_parameter='google_cloud_sender.line_price_reduce_taxexcl',
                                               default='True')
    line_price_reduce_taxinc = fields.Boolean(config_parameter='google_cloud_sender.line_price_reduce_taxinc',
                                              default='True')
    line_price_subtotal = fields.Boolean(config_parameter='google_cloud_sender.line_price_subtotal')
    line_price_tax = fields.Boolean(config_parameter='google_cloud_sender.line_price_tax')
    line_price_total = fields.Boolean(config_parameter='google_cloud_sender.line_price_total')
    line_price_unit = fields.Boolean(config_parameter='google_cloud_sender.line_price_unit')
    line_product_uom = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom')
    line_product_uom_category_id = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom_category_id',
                                                  default='True')
    line_product_uom_qty = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom_qty')
    line_product_updatable = fields.Boolean(config_parameter='google_cloud_sender.line_product_updatable',
                                            default='True')
    line_qty_delivered = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered')
    line_qty_delivered_manual = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered_manual',
                                               default='True')
    line_qty_delivered_method = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered_method',
                                               default='True')

    order_id = fields.Boolean(config_parameter='google_cloud_sender.order_id')
    name = fields.Boolean(config_parameter='google_cloud_sender.name')

    credentials_json = fields.Binary('Credenciales OAuth Json', related='company_id.credentials_json', readonly=False)
    make_file_public = fields.Boolean(string="Hacer el fichero público", config_parameter='google_cloud_sender.make_file_public')
    bucket = fields.Char(string="Bucket", config_parameter='google_cloud_sender.bucket')

