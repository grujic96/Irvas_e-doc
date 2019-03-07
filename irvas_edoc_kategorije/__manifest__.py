# -*- coding: utf-8 -*-

{
    'name': 'irvas_edoc_kategorije',
    'version': '1.0.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'EDOC',
    'complexity': "easy",
    'description': """
        Model opste liste kategorija dokumentarnog materijala sa rokovima cuvanja
    """,
    'author': 'Aleksandar Grujic',
    'website': 'http://www.irvas_edoc.org',
    'depends': [],
    'data': [
        'views/irvas_edoc_kategorije.xml',
        'views/irvas_edoc_demo.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 100,
    'currency': 'EUR',
    'license': 'OPL-1',
    'live_test_url': 'https://www.openeducat.org/plans'
}
