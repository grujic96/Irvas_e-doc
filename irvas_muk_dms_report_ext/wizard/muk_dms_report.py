# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from itertools import groupby
from operator import itemgetter
from collections import defaultdict
import logging
_logger = logging.getLogger(__name__)


class MukDmsFileReportLine(models.TransientModel):
	_name = 'muk_dms.file.report.line'

	wizard_id = fields.Many2one('muk_dms.file.report', required=True, ondelete='cascade')
	name = fields.Char(required=False, string="Label")
	document_id = fields.Many2one('muk_dms.file',string="Dokument")

	sub_number = fields.Integer()
	basic_number = fields.Integer()

	document_number = fields.Text(string='Document Number')

	contact_id = fields.Many2one(related='document_id.contact_id')
	contact_name = fields.Char()

	object = fields.Text()
	document_class_id = fields.Many2one(related='document_id.document_class_id')
	document_name = fields.Text()

	date_receive = fields.Datetime(related='document_id.date_receive')
	date_shipped = fields.Datetime(related='document_id.date_shipped')

	document_type = fields.Text()
	date_shipped_receive = fields.Datetime()

class DmsReport(models.TransientModel):
	_name = 'muk_dms.file.report'
	_description = 'Wizard that opens document report'

	date = fields.Date(string='Od Datuma')
	date_finish = fields.Date(string="Do Datuma")
	document_state = fields.Selection([('prijem', 'Prijem'), ('otprema', 'Otprema')])
	document_ids = fields.One2many('muk_dms.file.report.line','wizard_id',required=True,ondelete='cascade')



	@api.multi
	def print_pdf_document_report(self):

		for wizard_id in self.env['muk_dms.file.report.line'].search([('wizard_id','=',self.id)]):
			if wizard_id.wizard_id.id == self.id:
				self.write({'document_ids': [(3, wizard_id.id)]})

		document_ids_filtered = []
		document_ids =[]
		date_shipped_receive = None
		for resource in self.env['muk_dms.file'].search([('document_state','=',self.document_state)]):
			if self.document_state == 'prijem':
				date_shipped_receive = resource.date_receive

			else:
				date_shipped_receive = resource.date_shipped

			print(resource.document_class_id.id)
			print(date_shipped_receive)
			if self.date <= resource.create_date and resource.create_date <= self.date_finish:
				document_ids_filtered.append({
					'name': resource.name,
					'create_date': resource.create_date,
					'sub_number': resource.sub_number,
					'basic_number': resource.basic_number,
					'contact_id': resource.contact_id,
					'document_name': resource.document_class_id.name,
					'date_shipped_receive': date_shipped_receive,
					'document_type': resource.document_class_id.document_type,
					'document_class_id': resource.document_class_id,
					'contact_name': resource.contact_id.name,
					'object': resource.object,
					'document_number': resource.document_number,
				})
		grouper = itemgetter("name", "create_date", "sub_number", "basic_number", "contact_id", "document_class_id", "date_shipped_receive","document_type","document_name","contact_name","object","document_number")
		_logger.warning('-------------------------------%s', grouper)
		for key, grp in groupby(sorted(document_ids_filtered, key=grouper), grouper):
			temp_dict = dict(zip(
				["name", "create_date", "sub_number", "basic_number", "contact_id", "document_class_id","date_shipped_receive","document_type","document_name","contact_name","object","document_number"], key))

			document_ids.append((0, 0, temp_dict))

		_logger.warning('------------------asdasdasdasdasd-------------%s', document_ids)


		if len(document_ids) == 0:
			raise ValidationError(('Nema documenata u zadatom periodu'))

		self.write({'document_ids': document_ids})
		context = {
			'lang': 'en_US',
			'active_ids': [self.id],
		}
		data=None
		print('stigooooooooooooooooooooooooooooo')
		return self.env.ref('irvas_muk_dms_report_ext.report_document'). \
			report_action(self, data=data)
