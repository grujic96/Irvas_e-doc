
from odoo import models, api, fields



class MukDmsExt(models.Model):
    _inherit = "muk_dms.file"


    object = fields.Text(string="Predmet")
    sub_number = fields.Integer(string="Pod Broj",store=True, compute='number_onchange')
    create_date = fields.Datetime(string="Datum")
    contact_id = fields.Many2one('res.partner',string="Posiljaoc")
    document_class_id = fields.Many2one('irvas.edoc.document.class', string="Klasa Dokumenta")


    def _get_number_id(self):
        print('usoooo')
        file = self.env['muk_dms.file'].search([])
        a=[]
        max_number= 0
        for f in file:
            a.append(f.basic_number)
        for i in range(len(a)):
            if a[i]> max_number:
                max_number = a[i]
            print(a[i])
        print(max_number)
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
