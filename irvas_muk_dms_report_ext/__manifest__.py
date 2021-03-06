# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2016 Shawn
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "irvas_muk_dms_report_ext",
    "author": "Aleksandar Grujic @Irvas",

    "category": "ext",
    "depends": [
        'muk_dms', 'irvas_muk_dms_document', 'irvas_edoc_kategorije'
    ],
    "data": [
        "report/nix_sit_history_report.xml",
        "report/muk_dms_report_view.xml",
        "wizard/muk_dms_wizard_view.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
