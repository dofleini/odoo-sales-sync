# -*- coding: utf-8 -*-
{

    'name': 'Google Cloud Sender',
    'category': 'Sales/Sales',

    'summary': 'Envia los datos de tus ventas a Google Cloud Storage como CSV',

    'version': '1.0',
    'description': "Envia los datos de tus ventas a Google Cloud Storage como CSV",

    'author': "Jaco",

    'depends': ['website_sale'],

    'data': [
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'auto_install': False

}