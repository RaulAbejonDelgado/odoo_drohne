from openerp import api ,models, fields,_
import openerp.http as http
from openerp.http import Response
import logging
import psycopg2
import json
import sys
reload(sys)

_logger = logging.getLogger(__name__)

class web_services(http.Controller):
    
    @http.route('/web/odoo/test', type='json', auth="none", methods=['POST'],cors="*", csrf=False)
    def listener(self, **kw):

        print http.request.params
        print "**************"
        return json.dumps({"result":"Success"})
    
    @http.route('/web/odoo/demo_html', type="http") 
    def res_html(self):
        return "<h1>This is a test</h1>"
    
    @http.route('/web/odoo/demo_json', type="json", methods=['POST'], cors="*",auth="none")
    def res_json(self , **kw):
        print("jur jur")
        return [{"sample_dictionary": "This is a sample JSON dictionary"}]
    