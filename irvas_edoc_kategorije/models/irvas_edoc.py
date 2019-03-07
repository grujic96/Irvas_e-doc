
from odoo import models, api, fields


class IrvasEdocCategories(models.Model):

    _name = 'irvas.edoc.categories'

    name = fields.Text(string="Kategorija registarskog materijala")
    saving_time_limit = fields.Text(string="Rok cuvanja")
    description = fields.Text(string="Napomene sa objasnjenjem; detaljnije razvrstavanje")
    subgroup_id = fields.Many2one('irvas.edoc.subgroup', string='Podgrupa')
    group_id = fields.Many2one('irvas.edoc.group', string="Grupa")
    main_group_id = fields.Many2one('irvas.edoc.main.group', string='Glavna Grupa')

    main_group_id_number = fields.Integer(string="Glavna Grupa", related='main_group_id.number')
    group_id_number = fields.Integer(string="Grupa", related='group_id.number')
    subgroup_id_number = fields.Integer(string="Podgrupa", related='subgroup_id.number')


    @api.onchange('group_id')
    def on_change_group(self):
        if self.subgroup_id != None:
            group_id = self.group_id
            main_group_id = self.main_group_id
            self.subgroup_id = None
            self.group_id = group_id
            self.main_group_id = main_group_id


class IrvasEdocDocumentClass(models.Model):

    _name = 'irvas.edoc.document.class'

    name = fields.Text(string='Klasa Dokumenta')

    irvas_edoc_category_id = fields.Many2one('irvas.edoc.categories',string="Kategorija registarskog materijala")

    main_group_id = fields.Many2one(string='Glavna Grupa', related='irvas_edoc_category_id.main_group_id', default=None)
    group_id = fields.Many2one(string='Grupa', related='irvas_edoc_category_id.group_id', default=None)
    subgroup_id = fields.Many2one(string='Podgrupa', related='irvas_edoc_category_id.subgroup_id', default=None)

    document_type = fields.Selection([('ulazni', 'Ulazni'), ('izlazni', 'Izlazni'), ('interni', 'Interni')])


class IrvasEdocMainGroup(models.Model):

    _name = 'irvas.edoc.main.group'

    name = fields.Text(string='Ime Glavne Grupe')
    number = fields.Integer(string="Glavna Grupa")

    _sql_constraints = [
        ('main_group_number_unique', 'unique (number)', 'Main group number must be unique!')]

class IrvasEdocGroup(models.Model):

    _name = 'irvas.edoc.group'

    name = fields.Text(string='Ime Grupe')
    number = fields.Integer(string="Grupa")

    main_group_id = fields.Many2one('irvas.edoc.main.group', string='Glavna Grupa')
    main_group_id_number = fields.Integer(string="Glavna Grupa", related ='main_group_id.number')

class IrvasEdocSubgroup(models.Model):

    _name = 'irvas.edoc.subgroup'

    name = fields.Text(string='Ime Podgrupe')
    number = fields.Integer(string="Podgrupa")

    group_id = fields.Many2one('irvas.edoc.group', string='Grupa')
    main_group_id = fields.Many2one(string='Glavna Grupa', related='group_id.main_group_id')

    group_id_number = fields.Integer(string="Grupa", related='group_id.number')
    main_group_id_number = fields.Integer(string="Glavna Grupa", related='group_id.main_group_id_number')