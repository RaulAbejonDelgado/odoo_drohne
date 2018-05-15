# -*- encoding: utf-8 -*-
##############################################################################
#
#    Kernet - Address Region module for OpenERP
#    Copyright (C) 2016 José Javier Goyos Madriz
#
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


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
