# -*- coding: utf-8 -*-
#!/usr/bin/python
from openerp import api ,models, fields,_
import psycopg2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    external_id = fields.Integer('External id')
    
    notify_email= fields.Selection([
            ('none', 'Never'),
            ('always', 'All Messages'),
            ], 'Receive Inbox Notifications by Email', required=False,
            oldname='notification_email_send',
            help="Policy to receive emails for new messages pushed to your personal Inbox:\n"
                    "- Never: no emails are sent\n"
                    "- All Messages: for every notification you receive in your Inbox"),

    _defaults = {
        'notify_email': lambda *args: 'none'
    }
    
class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    
    external_id = fields.Integer('External id')
    
# class ProductTemplate(models.Model):
#     _inherit = 'product.template'
#     
#     external_id = fields.Integer('External id')
    
# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#     
#     external_id = fields.Integer('External id')
#     
# class AccountAccount(models.Model):
#     _inherit = 'account.account'
#     
#     external_id = fields.Integer('External id')