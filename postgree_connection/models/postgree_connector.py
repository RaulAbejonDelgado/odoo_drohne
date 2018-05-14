# -*- coding: utf-8 -*-
#!/usr/bin/python
from openerp import api ,models, fields,_
import psycopg2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class postgree_connector(models.Model):
    _name = 'postgree.connector'

    name = fields.Char('Nombre de la conexion')
    source_server = fields.Char('host origen')
    source_db = fields.Char('Base de datos origen')
    source_user = fields.Char('Usuario origen')
    source_pass = fields.Char('Password')
    source_table_name = fields.Char('Nombre del modelo/tabla origen')
    dest_server = fields.Char('host destino')
    dest_db = fields.Char('Base de datos destino')
    dest_user = fields.Char('Usuario de la base de datos destino')
    dest_table = fields.Char('Modelo destino')
    connection_result = fields.Boolean('Conexion establecida ?')
    connection_message = fields.Char('Mensaje de servidor')
    
#     @api.multi
#     def UnlinkItems(self):
# #         self.ensure_one()
# #         obj_to_delete = self.env['ir.model'].search([('name','=','kernet_'+str(self.source_table_name))])
# #         if obj_to_delete.field_id:
# #             for field in obj_to_delete.field_id:
# #                 field.unlink()
# #         if obj_to_delete:
# #             obj_to_delete.unlink()
#         conn = self.ConnectPostgOrig()
#         cur = conn.cursor()
#         cur.execute("DROP TABLE kernet_'{0}".format(table_name))  
#         conn.commit()
#         conn.close()
        
    @api.multi
    def UpdateData(self,obj_dict):
        """Recibe un diccionario con valores proviniente de la tabla destino"""
        for s in self:
            obj_id = self.env[s.dest_table].search([('models','=',obj_dict['models'])])
            if not obj_id:
                obj_id.create(dict)
            if obj_id:
                obj_id.write(dict)
    
    @api.multi
    def ConnectPostgOrig(self):
        #Se define el string de conexion en base a los datos del formulario
        for s in self:
            conn_string = "host={0} user={1} dbname={2} password={3}".format(s.source_server, s.source_user, s.source_db, s.source_pass)
            conn = psycopg2.connect(conn_string)
            return conn 
    
    @api.multi
    def Conecction(self):
        for s in self:
            #se comprueban los datos de conexion si ok establece connexion y rellena campos informativos del formulario, obtenemos la conexion
            conn = s.ConnectPostgOrig()
            #llamo al metodo que me devuelve la estructura de la tabla seleccionada,pasandole conn, para que haga consulta sql en la bd/tabla origen
            #list_key = lista con los nombres de los campos de la tabla
            list_key = s.GetStructure(conn)
            model = s.GetModel(s.source_table_name,list_key)
            lists_values = s.GetData(conn,s.source_table_name,list_key)

                    
#             for partner_listn in list_value:
#                 for partner_data in partner_listn:
#                     dict[partner_value] = partner_value
    @api.multi
    def UpdateFieldsOnModel(self,list_key,res):
        for s in self:
            for field in list_key:
                field_id = s.env['ir.model.fields'].search(['&',('name','=',field[0]),('model_id','=',res.id),('modules','=','postgree_connection')])
                fields_vals = {
                        'name':str(field[0]),
                        'field_description':str(field[0]),
                        'ttype':'char',
                        'state':'base',
                        'model_id':res.id,
                        'modules':'postgree_connection',
                        }        
                if field_id and field_id.name != 'uos_coeff' or field_id.name != 'active':
                    print field_id.name
                    field_id.write(fields_vals)
                if not field_id:
                    field_id.create(fields_vals)
                

    @api.multi
    def GetModel(self,table,list_key):
        for s in self:
            #table_convert = 'kernet_'+str(table)
            model_obj = s.env['ir.model'].search([('model','=','kernet.'+str(table))])
            model_vals = {
                'name':'kernet_'+str(table),
                'model':'kernet.'+str(table),
                'state':'base',
                'osv_memory':False,
                }
            if not model_obj:
                res = model_obj.create(model_vals)
                s.UpdateFieldsOnModel(list_key,res)
                return res
            if model_obj:
                model_obj.write(model_vals)
                s.UpdateFieldsOnModel(list_key,model_obj)
                return model_obj
    
    @api.multi
    def ConnectionMessage(self):
        for s in self:
            conn = self.ConnectPostgOrig()
            if conn:
                s.connection_message = str(conn)
                s.connection_result = True
                return conn
            if not conn:
                s.connection_message = 'No se ha podido establecer la conexion'
                s.connection_result = False
    
    @api.multi
    def GetStructure(self,conn):
        for s in self:
            cursor = conn.cursor()
            """ Obtenemos la estructura de la tabla origen y guardamos los datos
             en un diccionario, estos datos son las keys del diccionario.
             En el mismo proceso lo que seran las keys las guardo en una lista"""
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{0}'".format(s.source_table_name))
            #cr.execute('select * from res_partner where name = %s', (partner_name,))
            rows = cursor.fetchall()
            dict = {}
            list_key = []
            #Guardo la estructura de la tabla elegida siendo todos los campos Char
            for field in rows: 
                dict[str(field[0])] = ''
                list_key.append(field)
            return list_key
        
    
    def GetData(self,conn,table_name,list_key):
        """conn: objeto con la conexion establecida a la db
        table_name: Nombre de la tabla a la que haremos consulta para obtener los datos
        list_key: Lista con las claves, para la creacion del diccionario
        Devuelve list_of_dicts = una lista con diccionarios, cada diccionario tiene la clave:valor de la tabla original """
        cursor = conn.cursor()
        dict = {}
        list_of_dicts = []
        #cojo el contenido de la tabla elegida
#         cursor.execute("SELECT * FROM {0}".format(table_name))
#         tables_values =  cursor.fetchall()
#         for table_value in tables_values:
#             for field_key,field_value in zip(list_key,table_value):
#             list_of_dicts.append(dict) 
#         return list_of_dicts
