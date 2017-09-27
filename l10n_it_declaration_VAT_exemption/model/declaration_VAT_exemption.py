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
from openerp import models, fields, api
from openerp.osv import osv


class res_partner(models.Model):
    _inherit = "res.partner"
    _description = "Declaration declaration of VAT exemption"

    #esenzione iva
    declaration_exemption_vat = fields.Char('N.Decl.VAT Exemption customer',
        help="Number Declaration VAT Exemption customer")
    protocol_declaration_exemption_vat = fields.Char(
        'Internal protocol VAT exemption',
        help="Number of internal protocol for the_registration of the declaration of VAT exemption")
    date_declaration_exemption_vat = fields.Date('Declaration Date',
        help="Date of declaration of the customer for the VAT exemption")
    date_internal_protocol_exemption_vat = fields.Date('Date internal protocol',
        help="Date of internal protocol for the registration of the declaration of VAT exemption")
res_partner()



class account_invoice(models.Model):
    _inherit = "account.invoice"
    #invoice directly

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        if not partner_id:
            return {'value': {
            'account_id': False,
            'payment_term': False,
            'declaration_exemption_vat': '',
            'protocol_declaration_exemption_vat': '',
            'date_declaration_exemption_vat': False,
            'date_internal_protocol_exemption_vat': False,
            }
        }

        result =  super(account_invoice, self).onchange_partner_id(type, partner_id,
            date_invoice ,payment_term, partner_bank_id, company_id)
        valori=result.get('value',{})

        partner = self.env['res.partner'].browse(partner_id)
        if partner.parent_id:
            partner = partner.parent_id
        
        valori['declaration_exemption_vat']=(
            partner.declaration_exemption_vat and partner.declaration_exemption_vat or '')
        valori['protocol_declaration_exemption_vat']=(
            partner.protocol_declaration_exemption_vat and partner.protocol_declaration_exemption_vat or '')
        valori['date_declaration_exemption_vat']=(
            partner.date_declaration_exemption_vat and partner.date_declaration_exemption_vat or False)
        valori['date_internal_protocol_exemption_vat']=(
            partner.date_internal_protocol_exemption_vat and partner.date_internal_protocol_exemption_vat or False)
        return {'value': valori}


    declaration_exemption_vat = fields.Char('N.Decl.VAT Exemption customer',
        help="Number Declaration VAT Exemption customer")
    protocol_declaration_exemption_vat = fields.Char('Internal protocol VAT exemption',
        help="Number of internal protocol for the registration of the declaration of VAT exemption")
    date_declaration_exemption_vat = fields.Date('Declaration Date',
        help="Date of declaration of the customer for the VAT exemption")
    date_internal_protocol_exemption_vat = fields.Date('Date internal protocol',
        help="Date of internal protocol for the registration of the declaration of VAT exemption")


class stock_picking(osv.osv):
    #fatturazione da ordine di consegna
    _inherit = "stock.picking"

    def action_invoice_create(self, cr, uid, ids, journal_id=False, group=False, type='out_invoice', context=None):
        res = super(stock_picking, self).action_invoice_create(
            cr, uid, ids, journal_id, group, type, context)
        for id_invoice in res:
            invoice = self.pool.get('account.invoice').browse(cr, uid, id_invoice)
            vals={}
            if invoice.partner_id.parent_id:
                partner = invoice.partner_id.parent_id
            else:
                partner = invoice.partner_id
            if partner.declaration_exemption_vat:
                vals['declaration_exemption_vat']=partner.declaration_exemption_vat
            if partner.protocol_declaration_exemption_vat:
                vals['protocol_declaration_exemption_vat']=partner.protocol_declaration_exemption_vat
            if partner.date_declaration_exemption_vat:
                vals['date_declaration_exemption_vat']=partner.date_declaration_exemption_vat
            if partner.date_internal_protocol_exemption_vat:
                vals['date_internal_protocol_exemption_vat']=partner.date_internal_protocol_exemption_vat
            invoice.write(vals)

        return res




class sale_order(osv.osv):
    _inherit = "sale.order"
    #fatturazione da ordine di vendita

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        invoice_vals=super(sale_order, self)._prepare_invoice( cr, uid, order, lines, context)
        
        partner = self.pool.get('res.partner').browse(cr, uid, invoice_vals['partner_id'])
        if partner.parent_id:
            partner = partner.parent_id

        if partner.declaration_exemption_vat:
            invoice_vals['declaration_exemption_vat']=partner.declaration_exemption_vat
        if partner.protocol_declaration_exemption_vat:
            invoice_vals['protocol_declaration_exemption_vat']=partner.protocol_declaration_exemption_vat
        if partner.date_declaration_exemption_vat:
            invoice_vals['date_declaration_exemption_vat']=partner.date_declaration_exemption_vat
        if partner.date_internal_protocol_exemption_vat:
            invoice_vals['date_internal_protocol_exemption_vat']=partner.date_internal_protocol_exemption_vat

        return invoice_vals
sale_order()


class sale_advance_payment_inv(osv.osv_memory):
    _inherit = "sale.advance.payment.inv"
    #fatturazione in percentuale o a valore
    def _prepare_advance_invoice_vals(self, cr, uid, ids, context=None):
        res=super(sale_advance_payment_inv, self)._prepare_advance_invoice_vals(cr, uid, ids, context)
        for sel_order in res:
            invoice = sel_order[1]
            partner_id=invoice['partner_id']
            
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
            if partner.parent_id:
                partner = partner.parent_id
                
            if partner.declaration_exemption_vat:
                invoice['declaration_exemption_vat']=partner.declaration_exemption_vat
            if partner.protocol_declaration_exemption_vat:
                invoice['protocol_declaration_exemption_vat']=partner.protocol_declaration_exemption_vat
            if partner.date_declaration_exemption_vat:
                invoice['date_declaration_exemption_vat']=partner.date_declaration_exemption_vat
            if partner.date_internal_protocol_exemption_vat:
                invoice['date_internal_protocol_exemption_vat']=partner.date_internal_protocol_exemption_vat    
        return res
sale_advance_payment_inv()   


class sale_order_line_make_invoice(osv.osv_memory):
    _inherit = "sale.order.line.make.invoice"
    #fatturazione righe ordine
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res=super(sale_order_line_make_invoice, self)._prepare_invoice(cr, uid, order, lines, context)
        
        partner = self.pool.get('res.partner').browse(cr, uid, res['partner_id'])
        if partner.parent_id:
           partner = partner.parent_id
                
        if partner.declaration_exemption_vat:
            res['declaration_exemption_vat']=partner.declaration_exemption_vat
        if partner.protocol_declaration_exemption_vat:
            res['protocol_declaration_exemption_vat']=partner.protocol_declaration_exemption_vat
        if partner.date_declaration_exemption_vat:
            res['date_declaration_exemption_vat']=partner.date_declaration_exemption_vat
        if partner.date_internal_protocol_exemption_vat:
            res['date_internal_protocol_exemption_vat']=partner.date_internal_protocol_exemption_vat
        
        return res
sale_order_line_make_invoice()     
     
