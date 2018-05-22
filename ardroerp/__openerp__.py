{
    'name': 'Ardroerp',
    'version': '1.0',
    'category': 'hardware',
    'author': 'ItOpen',
    'description': 'Digital output arduino control',
    'website': 'http://www.itopen.it',
    'contributors': [
        'Raul Abejon Delgado <raul.abejon.delgado@gmail.com>',
    ],
    'depends': ['base'],
    'data' : [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/arduinocontroller_views.xml',
    ],
    'external_dependencies' : {
            'python': ['pyfirmata']
    },
    'active': False,
    'installable': True,
}
