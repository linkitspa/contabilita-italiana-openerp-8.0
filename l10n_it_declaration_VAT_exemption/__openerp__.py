# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (C) 2015 Link It spa
#    (<http://www.linkgroup.it/>).
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
{'name': 'Link it- localizzazione italiana - l10n_it_declaration_VAT_exemption',
 'version': '0.1',
 'depends': ['base', 'account', 'sale', 'stock', 'stock_account'],
 'description': """\
       Aggiunge i seguenti campi sull'anagrafica cliente:
        - dichiarazione_esenzione_iva
        - protocollo_dichiarazione_esenzione_iva
        - data_dichiarazione_esenzione_iva
        - data_protocollo_interno_esenzione_iva
        I campi vengono poi memorizzati in fattura in questi tre casi:
        - fatturazione diretta
        - fatturazione ordine di vendita
        - fatturazione ordine di consegna
        """,
 'author': 'Link It spa',
 'website': 'http://www.linkgroup.it',       
 'init_xml': [],
 'update_xml': [],
 'data': ['view/VAT_exemption_view.xml'],
 'demo_xml': [],
 'tests': [],
 'installable': True,
 'images': [],
 'auto_install': False,
 'application': True
}