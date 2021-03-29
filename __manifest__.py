# -*- coding: utf-8 -*-
{
    'name': "Stock transfer",
    'summary': """ Stock transfer """,
    'description': """
        Stock transfer
    """,
    'author': "Aquih",
    'website': "http://www.aquih.com",
    'category': 'Operations/Inventory',
    'version': '1.0',
    'depends': ['stock'],
    'data': [
        'views/stock_views.xml',
        'security/stock_transfer_security.xml',
    ],
}
