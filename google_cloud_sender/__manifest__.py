# -*- coding: utf-8 -*-
{

    'name': 'Odoo Sales Sync',
    'category': 'Sales/Sales',

    'summary': 'Envia los datos de tus ventas a Google Cloud Storage como CSV',

    'version': '1.01',
    'description': "Envia los datos de tus ventas a Google Cloud Storage como CSV",

    'author': "Jaco",

    'depends': ['website_sale'],
    "external_dependencies": {"python": ["gcloud"]},

    "images": ['static/description/icon.png', 'static/images/thumbnail.png'],

    'data': [
        'data/cron.xml',

        'views/res_config_settings_views.xml',
        'views/cron_log_view.xml',
        'views/menu.xml',

        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [],

    'installable': True,
    'auto_install': False,
    'application': True,
}
