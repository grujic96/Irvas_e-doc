
from odoo import models, api, fields



class MukDmsExt(models.Model):
    _inherit = "muk_dms.file"

    object = fields.Text(string="Predmet")
    sub_number = fields.Integer(string="Pod Broj",store=True, compute='number_onchange')
    create_date = fields.Datetime(string="Datum")
    contact_id = fields.Many2one('res.partner',string="Posiljaoc")
    document_class_id = fields.Many2one('irvas.edoc.document.class', string="Klasa Dokumenta")
    date_receive = fields.Datetime(string="Datum Prijema")
    date_shipped = fields.Datetime(string="Datum Otpreme")

    digital_signature = fields.Binary(string="Digital Signature")
    #received_type = fields.Selection([('on_hands', 'On Booking'),
     #                                ('manual', 'On Check In'),
      #                               ('picking', 'On Checkout')], description='The way document was received', string="Receive Type")


    def _set_document_type(self):
        self.document_type = self._context.get('document_type')

    document_type = fields.Selection([('prijem','Prijem'), ('otprema','Otprema')], default=_set_document_type, store=True, readonly=True)


    def _get_number_id(self):
        file = self.env['muk_dms.file'].search([])
        a=[]
        max_number= 0
        for f in file:
            a.append(f.basic_number)
        for i in range(len(a)):
            if a[i]> max_number:
                max_number = a[i]
        if max_number == 0:
            return 1
        else:
            return max_number + 1

    basic_number = fields.Integer(string="Osnovni Broj", default=_get_number_id, store=True, readonly=False)

    @api.one
    @api.depends('basic_number')
    def number_onchange(self):
        file = self.env['muk_dms.file'].search([('basic_number', '=', self.basic_number)])
        if file is None:
            self.basic_number = 1
            self.sub_number = 1
        else:
            max_subnumber=0
            for f in file:
                if f.sub_number > max_subnumber:
                    max_subnumber = f.sub_number
            self.sub_number = max_subnumber + 1


    def open_create_document_received(self,ctx, context=None):
        context=ctx
        print(context)
        print(context.get('izlazni'))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'muk_dms.file',
            'view_mode': 'form',
            'target': 'current',
            'context': context,
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'create'}}}
        }

    def open_create_document_shipping(self,ctx, context=None):
        context=ctx

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'muk_dms.file',
            'view_mode': 'form',
            'target': 'current',
            'context': context,
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'create'}}}
        }

    # @api.onchange('location_dest_id')
    # def get_document_type(self, context=None):
    #     if self.location_dest_id:
    #         res = {}
    #         micro_list = []
    #
    #         if 'sit_prelociranje_form_action' in self._context:
    #             micro_location = self.env['stock.microlocation'].search(
    #                 [('stock_location_id', '=', self.location_dest_id.id)], limit=1)
    #             # self.micro_loc_dest_id = micro_location.id
    #             micro_location_obj = self.env['stock.microlocation']
    #             micro_location_ids = micro_location_obj.search([('stock_location_id', '=', self.location_dest_id.id)])
    #             for record in micro_location_ids:
    #                 micro_list.append(record.id)
    #             res = {'domain': {'micro_loc_dest_id': [('id', 'in', micro_list)]}}
    #             return res
    #
    #         if 'sit_trebovanje_form_action' in self._context:
    #             micro_location_obj = self.env['stock.microlocation']
    #             micro_location_ids = micro_location_obj.search([[u'stock_location_id.name', u'ilike', u'SI u upotrebi'],
    #                                                             ('stock_location_id.usage', '=', 'asset')])
    #             for record in micro_location_ids:
    #                 micro_list.append(record.id)
    #             res = {'domain': {'micro_loc_dest_id': [('id', 'in', micro_list)]}}



