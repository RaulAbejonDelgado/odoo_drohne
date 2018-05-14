# -*- coding: utf-8 -*-
#!/usr/bin/python
from openerp import api ,models, fields,_


class Empleado(models.Model):
    """ Modelo que redefine los metodos de los constraint para mejorar el rendimiento de la creacion de cuentas"""
    _name = 'empleado'

    name = fields.Char('name')
    Apellido = fields.Char('Apellido')
    IDDepartamento = fields.Many2one('departamento')
    
class Departamento(models.Model):
    """ Modelo que redefine los metodos de los constraint para mejorar el rendimiento de la creacion de cuentas"""
    _name = 'departamento'

    name = fields.Char('name')
    NombreDepartamento = fields.Char('Departamento')
    IDdepartamento = fields.Char('IDDepartamento')
    
    
#     