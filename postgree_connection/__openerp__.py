# -*- encoding: utf-8 -*-



{
    'name': 'Postgree connector',
    'version': '0.1',
    'category': 'Base',
    'license': 'AGPL-3',
    'complexity': 'easy',
    'description': ("Migration tool"),
    'author': "Raul Abejon Delgado",
    'contributors': [
        'Raul Abejon Delgado <raul.abejon.delgado@gmail.com>',
    ],
    'summary': 'Migration tool',
    'website': '',
    'depends': ['base'],
    'init_xml': [],
    'demo_xml': [],
    'data': [
             #'security/ir.model.access.csv',
             'views/menu.xml',
             'views/postgre_connector.xml',

            ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
