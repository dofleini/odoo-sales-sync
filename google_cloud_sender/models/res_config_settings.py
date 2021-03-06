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

    # file
    file_path = fields.Char(string="Carpeta", config_parameter='google_cloud_sender.file_path')

    # linea de productos
    line_id = fields.Boolean(config_parameter='google_cloud_sender.line_id')
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
    line_price_reduce_taxexcl = fields.Boolean(config_parameter='google_cloud_sender.line_price_reduce_taxexcl')
    line_price_reduce_taxinc = fields.Boolean(config_parameter='google_cloud_sender.line_price_reduce_taxinc')
    line_price_subtotal = fields.Boolean(config_parameter='google_cloud_sender.line_price_subtotal')
    line_price_tax = fields.Boolean(config_parameter='google_cloud_sender.line_price_tax')
    line_price_total = fields.Boolean(config_parameter='google_cloud_sender.line_price_total')
    line_price_unit = fields.Boolean(config_parameter='google_cloud_sender.line_price_unit')
    line_product_uom = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom')
    line_product_uom_category_id = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom_category_id')
    line_product_uom_qty = fields.Boolean(config_parameter='google_cloud_sender.line_product_uom_qty')
    line_product_updatable = fields.Boolean(config_parameter='google_cloud_sender.line_product_updatable')
    line_qty_delivered = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered')
    line_qty_delivered_manual = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered_manual')
    line_qty_delivered_method = fields.Boolean(config_parameter='google_cloud_sender.line_qty_delivered_method')

    # Orden de venta
    order_id = fields.Boolean(config_parameter='google_cloud_sender.order_id')
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

    # Producto
    product_active = fields.Boolean(config_parameter='google_cloud_sender.product_active')
    product_activity_date_deadline = fields.Boolean(
        config_parameter='google_cloud_sender.product_activity_date_deadline')
    product_activity_exception_decoration = fields.Boolean(
        config_parameter='google_cloud_sender.product_activity_exception_decoration')
    product_activity_exception_icon = fields.Boolean(
        config_parameter='google_cloud_sender.product_activity_exception_icon')
    product_activity_ids = fields.Boolean(config_parameter='google_cloud_sender.product_activity_ids')
    product_activity_state = fields.Boolean(config_parameter='google_cloud_sender.product_activity_state')
    product_activity_summary = fields.Boolean(config_parameter='google_cloud_sender.product_activity_summary')
    product_activity_type_id = fields.Boolean(config_parameter='google_cloud_sender.product_activity_type_id')
    product_activity_user_id = fields.Boolean(config_parameter='google_cloud_sender.product_activity_user_id')
    product_alternative_product_ids = fields.Boolean(
        config_parameter='google_cloud_sender.product_alternative_product_ids')
    product_attribute_line_ids = fields.Boolean(config_parameter='google_cloud_sender.product_attribute_line_ids')
    product_barcode = fields.Boolean(config_parameter='google_cloud_sender.product_barcode')
    product_can_image_1024_be_zoomed = fields.Boolean(
        config_parameter='google_cloud_sender.product_can_image_1024_be_zoomed')
    product_can_image_variant_1024_be_zoomed = fields.Boolean(
        config_parameter='google_cloud_sender.product_can_image_variant_1024_be_zoomed')
    product_can_publish = fields.Boolean(config_parameter='google_cloud_sender.product_can_publish')
    product_categ_id = fields.Boolean(config_parameter='google_cloud_sender.product_categ_id')
    product_code = fields.Boolean(config_parameter='google_cloud_sender.product_code')
    product_color = fields.Boolean(config_parameter='google_cloud_sender.product_color')
    product_combination_indices = fields.Boolean(config_parameter='google_cloud_sender.product_combination_indices')
    product_company_id = fields.Boolean(config_parameter='google_cloud_sender.product_company_id')
    product_cost_currency_id = fields.Boolean(config_parameter='google_cloud_sender.product_cost_currency_id')
    product_create_date = fields.Boolean(config_parameter='google_cloud_sender.product_create_date')
    product_create_uid = fields.Boolean(config_parameter='google_cloud_sender.product_create_uid')
    product_currency_id = fields.Boolean(config_parameter='google_cloud_sender.product_currency_id')
    product_default_code = fields.Boolean(config_parameter='google_cloud_sender.product_default_code')
    product_description = fields.Boolean(config_parameter='google_cloud_sender.product_description')
    product_description_purchase = fields.Boolean(config_parameter='google_cloud_sender.product_description_purchase')
    product_description_sale = fields.Boolean(config_parameter='google_cloud_sender.product_description_sale')
    product_display_name = fields.Boolean(config_parameter='google_cloud_sender.product_display_name')
    product_expense_policy = fields.Boolean(config_parameter='google_cloud_sender.product_expense_policy')
    product_has_configurable_attributes = fields.Boolean(
        config_parameter='google_cloud_sender.product_has_configurable_attributes')
    product_id = fields.Boolean(config_parameter='google_cloud_sender.product_id')
    product_image_1024 = fields.Boolean(config_parameter='google_cloud_sender.product_image_1024')
    product_image_128 = fields.Boolean(config_parameter='google_cloud_sender.product_image_128')
    product_image_1920 = fields.Boolean(config_parameter='google_cloud_sender.product_image_1920')
    product_image_256 = fields.Boolean(config_parameter='google_cloud_sender.product_image_256')
    product_image_512 = fields.Boolean(config_parameter='google_cloud_sender.product_image_512')
    product_image_variant_1024 = fields.Boolean(config_parameter='google_cloud_sender.product_image_variant_1024')
    product_accessory_product_ids = fields.Boolean(config_parameter='google_cloud_sender.product_accessory_product_ids')

    # Cliente
    client_active = fields.Boolean(config_parameter='google_cloud_sender.client_active')
    client_active_lang_count = fields.Boolean(config_parameter='google_cloud_sender.client_active_lang_count')
    client_activity_date_deadline = fields.Boolean(config_parameter='google_cloud_sender.client_activity_date_deadline')
    client_activity_exception_decoration = fields.Boolean(
        config_parameter='google_cloud_sender.client_activity_exception_decoration')
    client_activity_exception_icon = fields.Boolean(
        config_parameter='google_cloud_sender.client_activity_exception_icon')
    client_activity_ids = fields.Boolean(config_parameter='google_cloud_sender.client_activity_ids')
    client_activity_state = fields.Boolean(config_parameter='google_cloud_sender.client_activity_state')
    client_activity_summary = fields.Boolean(config_parameter='google_cloud_sender.client_activity_summary')
    client_activity_type_id = fields.Boolean(config_parameter='google_cloud_sender.client_activity_type_id')
    client_activity_user_id = fields.Boolean(config_parameter='google_cloud_sender.client_activity_user_id')
    client_additional_info = fields.Boolean(config_parameter='google_cloud_sender.client_additional_info')
    client_bank_account_count = fields.Boolean(config_parameter='google_cloud_sender.client_bank_account_count')
    client_bank_ids = fields.Boolean(config_parameter='google_cloud_sender.client_bank_ids')
    client_can_publish = fields.Boolean(config_parameter='google_cloud_sender.client_can_publish')
    client_category_id = fields.Boolean(config_parameter='google_cloud_sender.client_category_id')
    client_channel_ids = fields.Boolean(config_parameter='google_cloud_sender.client_channel_ids')
    client_child_ids = fields.Boolean(config_parameter='google_cloud_sender.client_child_ids')
    client_city = fields.Boolean(config_parameter='google_cloud_sender.client_city')
    client_color = fields.Boolean(config_parameter='google_cloud_sender.client_color')
    client_comment = fields.Boolean(config_parameter='google_cloud_sender.client_comment')
    client_commercial_company_name = fields.Boolean(
        config_parameter='google_cloud_sender.client_commercial_company_name')
    client_commercial_partner_id = fields.Boolean(config_parameter='google_cloud_sender.client_commercial_partner_id')
    client_company_id = fields.Boolean(config_parameter='google_cloud_sender.client_company_id')
    client_company_name = fields.Boolean(config_parameter='google_cloud_sender.client_company_name')
    client_company_type = fields.Boolean(config_parameter='google_cloud_sender.client_company_type')
    client_contact_address = fields.Boolean(config_parameter='google_cloud_sender.client_contact_address')
    client_contract_ids = fields.Boolean(config_parameter='google_cloud_sender.client_contract_ids')
    client_country_id = fields.Boolean(config_parameter='google_cloud_sender.client_country_id')
    client_create_date = fields.Boolean(config_parameter='google_cloud_sender.client_create_date')
    client_create_uid = fields.Boolean(config_parameter='google_cloud_sender.client_create_uid')
    client_credit = fields.Boolean(config_parameter='google_cloud_sender.client_credit')
    client_credit_limit = fields.Boolean(config_parameter='google_cloud_sender.client_credit_limit')
    client_currency_id = fields.Boolean(config_parameter='google_cloud_sender.client_currency_id')
    client_customer_rank = fields.Boolean(config_parameter='google_cloud_sender.client_customer_rank')
    client_date = fields.Boolean(config_parameter='google_cloud_sender.client_date')
    client_debit = fields.Boolean(config_parameter='google_cloud_sender.client_debit')
    client_debit_limit = fields.Boolean(config_parameter='google_cloud_sender.client_debit_limit')
    client_display_name = fields.Boolean(config_parameter='google_cloud_sender.client_display_name')
    client_email = fields.Boolean(config_parameter='google_cloud_sender.client_email')
