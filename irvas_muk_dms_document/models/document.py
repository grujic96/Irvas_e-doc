
from odoo import models, api, fields
from datetime import datetime


class MukDmsExt(models.Model):
    _name = "muk_dms.document"

    name = fields.Text(string="Document", compute="get_document_name")

    sub_number = fields.Integer(string="Pod Broj",store=True, compute="number_onchange",readonly=1)
    date_document = fields.Datetime(string="Datum", store=True)
    contact_id = fields.Many2one('res.partner',string="Posiljaoc")
    document_class_id = fields.Many2one('irvas.edoc.document.class', string="Klasa Dokumenta")
    date_receive = fields.Datetime(string="Datum Prijema")
    date_shipped = fields.Datetime(string="Datum Otpreme")
    digital_signature = fields.Binary(string="Digital Signature")
    document_number = fields.Text(string="Document Number", compute="get_document_number", store=True, readonly=True)

    document_unique_name = fields.Char()
    file_id = fields.Many2one('muk_dms.file')
    thumbnail = fields.Binary(related='file_id.thumbnail')
    thumbnail_medium = fields.Binary(related='file_id.thumbnail')
    color = fields.Integer(related='file_id.color')

    subject_id = fields.Many2one('muk_dms.document.subject', string='Subject', default=None)
    basic_number = fields.Integer(related='subject_id.id', readonly=1)
    check_bn = fields.Boolean(default=False, store=True)
    tags = fields.Many2many(
        comodel_name='muk_dms.tag',
        relation='muk_dms_file_tag_rell',
        column1='fid',
        column2='tid',
        string='Tags')

    document_type = fields.Selection([('ulazni','Ulazni'),('izlazni','Izlazni'),('interni','Interni')])

    @api.one
    @api.depends('document_class_id')
    def _get_document_state(self):
        if self.document_type == 'izlazni':
            self.document_state = 'otprema'
            print('asd')
        elif (self.document_type == 'ulazni') or (self.document_class_id.document_type == 'interni'):
            self.document_state = 'prijem'
            print('uso')
        else:
            return None
    document_state = fields.Selection([('prijem', 'Prijem'), ('otprema', 'Otprema')],store=True, compute=_get_document_state)

    @api.one
    @api.depends('name')
    def number_onchange(self):
        if self.sub_number > 0:
            pass
        else:
            docs = self.env['muk_dms.document'].search(['&',('subject_id','=',self.subject_id.id),('document_state','=', self.document_state)])
            max_subnumber =1
            print(docs)
            print(len(docs))
            a=0
            if len(docs)==0:
                pass
            else:
                for doc in docs:
                    if doc.id == self.id:
                        a = 1
                        print('doc_sub')
                        print(doc.sub_number)
                        pass
                    else:
                        if max_subnumber<doc.sub_number:
                            max_subnumber = doc.sub_number
            if len(docs)>1:
                if a == 0:
                    pass
                else:
                    self.sub_number = max_subnumber + 1
            else:
                if a == 0:
                    pass
                else:
                    self.sub_number = max_subnumber
                    print('postavi vredonts')
                    self.check_bn =True
                    print('postavio')

            print('zavrsio')


    @api.one
    @api.depends('name')
    def get_document_number(self):
        self.document_number = str(self.basic_number) + "-" + str(self.sub_number) + '/' + str(datetime.now().year)
        print('usooooo')
        print(self.document_number)
        print('prosos')

    @api.one
    def get_document_name(self):
        if self.document_state == 'prijem':
            date_shipped_receive = self.date_receive
        else:
            date_shipped_receive = self.date_shipped
        self.name = "doc_" + str(self.contact_id.id) + "-" + str(self.document_class_id.id) + "/" + date_shipped_receive
#     @api.multi
#     def run_document_shipped_action_wizard(self):
#         action = self.env.ref('irvas_muk_dms_extension.irvas_edoc_document_shipped_action_wizard').read()[0]
#         return action
#
# class DocumentShippingActionWizard(models.TransientModel):
#     _name="muk_dms.file.shipping.wizard"
#
#     contact_id = fields.Many2one('res.partner')
#     date_shipped = fields.Datetime()
#     basic_number = fields.Integer(related='muk_dms_file_id.basic_number')
#     sub_number = fields.Integer(related='muk_dms_file_id.sub_number')
#
#
#     def _get_number_id(self):
#         file = self.env['muk_dms.file'].search([])
#         a=[]
#         max_number= 0
#         for f in file:
#             a.append(f.basic_number)
#         for i in range(len(a)):
#             if a[i]> max_number:
#                 max_number = a[i]
#         if max_number == 0:
#             return 1
#         else:
#             return max_number + 1
#
#     new_basic_number = fields.Integer(string="Osnovni Broj", default=_get_number_id, store=True, readonly=False)
#
#
#
#     new_sub_number = fields.Integer(store="True",compute='number_onchange')
#
#     @api.one
#     @api.depends('new_basic_number')
#     def number_onchange(self):
#         file = self.env['muk_dms.file'].search([('basic_number', '=', self.new_basic_number)])
#         if file is None:
#             self.new_basic_number = 1
#             self.new_sub_number = 1
#         else:
#             max_subnumber = 0
#             for f in file:
#                 if f.sub_number > max_subnumber:
#                     max_subnumber = f.sub_number
#             self.new_sub_number = max_subnumber + 1
#
#     def _get_file_id(self):
#
#         id = self.env.context.get('id')
#         file_id = self.env['muk_dms.file'].search([('id','=',id)])
#         return file_id
#
#
#     muk_dms_file_id = fields.Many2one('muk_dms.file', default=_get_file_id)
#
#     def set_document_shipping(self):
#         print(self.env.context.get('contact_id'))
#         print(self.env.context.get('muk_dms_file_id'))
    # self.date_receive = None
    #  self.document_state = 'otprema'
    # self.contact_id = self.env.context.get('contact_id')
    # self.date_shipped = self.env.context.get('date_shipped')

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


class DocumentSubject(models.Model):
    _name = 'muk_dms.document.subject'

    name = fields.Text()

class MukDmsFileInherit(models.Model):
    _inherit = 'muk_dms.file'

    document_id = fields.Many2one('muk_dms.document')
