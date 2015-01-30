# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import tools
import openerp.addons.decimal_precision as dp
from openerp.osv import fields,osv

class account_invoice_report(osv.osv):
    _inherit = "account.invoice.report"    
    
    _columns = {        
        'state_id': fields.many2one('res.country.state','Provincia', readonly=True),
        'cost_price_db': fields.float(string='Cost Price stored',
                                      digits_compute = dp.get_precision('Sale Price'))
    }
    
    def _from(self):
      return super(account_invoice_report, self)._from() + " LEFT JOIN res_partner pa ON pa.id = ai.partner_id"

    def _select(self):
        return  super(account_invoice_report, self)._select() + ", sub.state_id as state_id, sub.cost_price_db as cost_price_db"

    def _sub_select(self):
        return  super(account_invoice_report, self)._sub_select() + """
            , pa.state_id as state_id
            , SUM(pr.cost_price_db * ail.quantity / u.factor) as cost_price_db
            """

    def _group_by(self):
        return super(account_invoice_report, self)._group_by() + ", pa.state_id, pr.cost_price_db"
