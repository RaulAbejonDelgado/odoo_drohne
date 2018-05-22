# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import logging
_logger = logging.getLogger(__name__)
# Add 1 because crappy OE doesn't distinguish empty from 0
         
          
PINMODE_OUTPUT = 2
PINMODE_INPUT = 1
PIN_RANGE = {
    
    PINMODE_OUTPUT: (0, 1),
    PINMODE_INPUT: (0, 1),
}


DEBUG=True

if DEBUG:
    logger = logging.getLogger(__name__)
    def dbg(msg):
        logger.info(msg)
else:
    def dbg(msg):
        pass


class arduinocontroller_board(osv.osv):
    """ Arduino board with configuration """

    # store device connections
    device_store = {}
    device_iterator_store = {}
    
    digital_pindir_values = [(PINMODE_OUTPUT, 'Output')]
    #pwm_pindir_values = [(PINMODE_INPUT, 'Input'), (PINMODE_OUTPUT, 'Output'), (PINMODE_PWM, 'PWM Output'), (PINMODE_SERVO, 'Servo Output')]
    _name = "arduinocontroller.board"
    _description = "Arduino board"
    _rec_name = 'device'
    _columns = {
    
        'device': fields.char('Device', size=64, required=True),
        'model': fields.selection([('uno', 'Arduino uno')], 'Model', default='uno', required=True),
        'online': fields.boolean('Online'),

        # Digital
        
        'pind2dir': fields.selection(digital_pindir_values, 'Digital function'),
        'pind2value': fields.integer('ON = 1 , OFF = 0'),
        

        
       
    }

    _defaults = {
        'device': '/dev/ttyACM0',
        'model': 'uno',
        
        }
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):

        if context is None:
            context = {}
        
        result = super(arduinocontroller_board, self).read(cr, uid, ids, fields=fields, context=context, load=load)

        print "EJEM COURSE"
        
        for x in result:
            print x
            if 'id' in x:
                print x['id']
        _logger.info('------------DEF READ ARDUINO CONTROLLER------------')
        #if 'id' in result[0]:
        #    result=super(arduinocontroller_board,self).write(cr,uid,ids,vals, context=context)
        return result

    # Let's support multiple configurations for the same device!
    #_sql_constraints = [('unique_model_device', 'unique(model, device)', 'Model and device must be unique')]

    def in_range(self, pin, mode, value, fail_silently=True):
        """ Constraints the var in range """
        
        if mode == PINMODE_INPUT:
            return value
            _logger.info('------------DEF IN_RANGE ARDUINO CONTROLLER------------')
            _logger.info(pin)
            _logger.info(mode)
            _logger.info(PIN_RANGE)

        (PIN_RANGE[mode])
        bottom , top = PIN_RANGE[mode]
        _logger.info('------------DEF IN_RANGE ARDUINO bottom , top------------')
        _logger.info(bottom)
        _logger.info(top)
        _logger.info(PIN_RANGE)
        res = bottom <= value <= top
        if not res and not fail_silently:
            raise osv.except_osv('Value is out of range', 'Please check that value for pin %s is in range %d-%d.' % (pin, bottom, top))
        if res:
            return value
        if value < bottom:
            return bottom
        return top
        

    def onchange_pin(self, cr, uid, ids, pin, mode, value):
        """ Check range """
        self.in_range(pin, int(mode), value, False)
        return {'value': {pin: value}}
        

    def onchange_online(self, cr, uid, ids, online, device):
        """ Connect to the device and report status """        
        v={}
        if ids and online:
            try:
                from pyfirmata import Arduino, util
            except ImportError:
                return {'warning' : {'title' : 'Attention!', 'message' : 'Pyfirmata is not installed, arduino operations are disabled. You can install pyfirmata from hg clone ssh://hg@bitbucket.org/tino/pyfirmata'}}
            board = self._get_board(device)
            if not board:
                 return {'warning' : {'title' : 'Attention!', 'message' : 'Cannot communicate with Arduino, please check your connections and settings on device %s.' % device}}            
            
        return {'value':v}
        

    def _setup_board(self, board, device, **kwargs):
        """
        Set the board up and read/write values from the board
        @return values
        """
        from pyfirmata import Arduino, util
        try:
            self.device_iterator_store[device]
        except:
            self.device_iterator_store[device] = util.Iterator(board)
            self.device_iterator_store[device].start()        
             
        v = {}
        # Digital pins        
        for i in range(2, 14):
            if 'pind%ddir' % i in kwargs and 'pind%dvalue' % i in kwargs:
                try:
                    pinmode = int(kwargs['pind%ddir' % i])
                    pinvalue = kwargs['pind%dvalue' % i]
                    pinvalue = self.in_range(i, pinmode, pinvalue)
                    board.digital[i].mode = pinmode-1  # less 1: crappy OE
                    dbg('DIGITAL %d Setting mode to : %d' % (i, pinmode))
                    v['pind%dvalue' % i] = pinvalue
                    if pinmode == PINMODE_INPUT:
                        v['pind%dvalue' % i] = board.digital[i].read()
                        dbg('DIGITAL %d reads %s' % (i, v['pind%dvalue' % i]))                 
                    
                    elif pinmode == PINMODE_OUTPUT:
                        dbg('DIGITAL OUTPUT %d writes %s' % (i, pinvalue))
                        board.digital[i].write(pinvalue)                       
                except:
                    raise
                
        # Analog pins
        # TODO: writing      
        for i in range(0, 6):
            if 'pina%dactive' % i in kwargs and kwargs['pina%dactive' % i]:
                board.analog[i].mode = PINMODE_INPUT-1 # less 1: crappy OE
                try:
                    #board.analog[i].enable_reporting()
                    v['pina%dvalue' % i] = board.analog[i].read()
                    dbg('ANALOG %d reads %s' % (i, v['pina%dvalue' % i]))    
                except:
                    # TODO: better error handling
                    raise
            else:
                # TODO: something or delete the branch
                pass
                
        return v
        

    def _get_board(self, device):
        """
        Returns device connection, creates one if necessary
        @returns boolean true if board is online
        """
        from pyfirmata import Arduino, util   
        try:
            return self.device_store[device]
        except KeyError:
            try:
                board = Arduino(device)
                self.device_store[device] = board
                return board
            except util.serial.SerialException:
                return False
        

    def write(self, cr, uid, ids, vals, context=None):
        """
        Update redord(s) exist in {ids}, with new value provided in {vals}

        @param cr: A database cursor
        @param user: ID of the user currently logged in
        @param ids: list of record ids to update
        @param vals: dict of new values to be set
        @param context: context arguments, like lang, time zone

        @return: Returns True on success, False otherwise
        """

        from pyfirmata import util
        record = self.browse(cr, uid, ids[0], context=context)               
        try:
            if record.online:
                # Merge values into vals
                parms = dict([(k, getattr(vals, k, getattr(record, k, None))) for k in self._columns if k.startswith('pin')])
                board = self._get_board(record.device)
                if board:
                    parms.update(vals)
                    vals = self._setup_board(board, record.device, **parms)
        except util.serial.SerialException:
            raise osv.except_osv('Device is set online but cannot communicate with Arduino', 'Please check your connections and settings on device %s.' % record.device)
            
        res = super(arduinocontroller_board, self).write(cr, uid, ids, vals, context=context)
        return res

    def refresh_board(self, cr, uid, ids, context=None):
        """ Re-read values from the board """
        record = self.browse(cr, uid, ids[0], context=context)
        if not record.online:
            raise osv.except_osv('Device is offline','Device is offline, check the online flag.')
        board = self._get_board(record.device)
        if not board:
            raise osv.except_osv('Cannot communicate with Arduino', 'Please check your connections and settings on device %s.' % record.device)
        return True


        

arduinocontroller_board()

