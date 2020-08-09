# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # GCS Config
    credentials_json = fields.Binary('Credenciales OAuth Json', related='company_id.credentials_json', readonly=False)
    make_file_public = fields.Boolean(string="Hacer el fichero público",
                                      config_parameter='google_cloud_sender.make_file_public')
    bucket = fields.Char(string="Bucket", config_parameter='google_cloud_sender.bucket')

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

    # Orden de venta
    order_id = fields.Boolean(config_parameter='google_cloud_sender.order_id')
    order_last_update = fields.Boolean(config_parameter='google_cloud_sender.order_last_update')
    order_access_token = fields.Boolean(config_parameter='google_cloud_sender.order_access_token')
    order_access_url = fields.Boolean(config_parameter='google_cloud_sender.order_access_url')
    order_access_warning = fields.Boolean(config_parameter='google_cloud_sender.order_access_warning')
    order_activity_date_deadline = fields.Boolean(config_parameter='google_cloud_sender.order_activity_date_deadline')
    order_activity_exception_decoration = fields.Boolean(
        config_parameter='google_cloud_sender.order_activity_exception_decoration')
    order_activity_exception_icon = fields.Boolean(config_parameter='google_cloud_sender.order_activity_exception_icon')
    order_activity_ids = fields.Boolean(config_parameter='google_cloud_sender.order_activity_ids')
    order_activity_state = fields.Boolean(config_parameter='google_cloud_sender.order_activity_state')
    order_activity_summary = fields.Boolean(config_parameter='google_cloud_sender.order_activity_summary')
    order_activity_type_id = fields.Boolean(config_parameter='google_cloud_sender.order_activity_type_id')
    order_activity_user_id = fields.Boolean(config_parameter='google_cloud_sender.order_activity_user_id')
    order_amount_by_group = fields.Boolean(config_parameter='google_cloud_sender.order_amount_by_group')
    order_amount_tax = fields.Boolean(config_parameter='google_cloud_sender.order_amount_tax')
    order_amount_total = fields.Boolean(config_parameter='google_cloud_sender.order_amount_total')
    order_amount_undiscounted = fields.Boolean(config_parameter='google_cloud_sender.order_amount_undiscounted')
    order_amount_untaxed = fields.Boolean(config_parameter='google_cloud_sender.order_amount_untaxed')
    order_analytic_account_id = fields.Boolean(config_parameter='google_cloud_sender.order_analytic_account_id')
    order_authorized_transaction_ids = fields.Boolean(
        config_parameter='google_cloud_sender.order_authorized_transaction_ids')
    order_campaign_id = fields.Boolean(config_parameter='google_cloud_sender.order_campaign_id')
    order_cart_quantity = fields.Boolean(config_parameter='google_cloud_sender.order_cart_quantity')
    order_cart_recovery_email_sent = fields.Boolean(
        config_parameter='google_cloud_sender.order_cart_recovery_email_sent')
    order_client_order_ref = fields.Boolean(config_parameter='google_cloud_sender.order_client_order_ref')
    order_commitment_date = fields.Boolean(config_parameter='google_cloud_sender.order_commitment_date')
    order_company_id = fields.Boolean(config_parameter='google_cloud_sender.order_company_id')
    order_create_date = fields.Boolean(config_parameter='google_cloud_sender.order_create_date')
    order_create_uid = fields.Boolean(config_parameter='google_cloud_sender.order_create_uid')
    order_currency_id = fields.Boolean(config_parameter='google_cloud_sender.order_currency_id')
    order_currency_rate = fields.Boolean(config_parameter='google_cloud_sender.order_currency_rate')
    order_date_order = fields.Boolean(config_parameter='google_cloud_sender.order_date_order')
    order_display_name = fields.Boolean(config_parameter='google_cloud_sender.order_display_name')
    order_expected_date = fields.Boolean(config_parameter='google_cloud_sender.order_expected_date')
    order_fiscal_position_id = fields.Boolean(config_parameter='google_cloud_sender.order_fiscal_position_id')
    order_invoice_count = fields.Boolean(config_parameter='google_cloud_sender.order_invoice_count')
    order_invoice_ids = fields.Boolean(config_parameter='google_cloud_sender.order_invoice_ids')
    order_invoice_status = fields.Boolean(config_parameter='google_cloud_sender.order_invoice_status')
    order_is_abandoned_cart = fields.Boolean(config_parameter='google_cloud_sender.order_is_abandoned_cart')
    order_is_expired = fields.Boolean(config_parameter='google_cloud_sender.order_is_expired')
    order_medium_id = fields.Boolean(config_parameter='google_cloud_sender.order_medium_id')
