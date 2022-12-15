Importing data on Tryton using proteus
Getting started
1/ pip install proteus==6.0.0
2/ open the terminal, inside the virtual environment type this command to execute the script contain the data that you have prepared:
python3 path/to/yourscript.py -c /path/to/your/configuration/file -d database name

3/Coding Part :
Here an example of a script that i have made by my self for testing in my localhost to import 2 invoices data.
the first invoice on state "Draft", the 2nd invoice on state "Posted"

                                     ****FIND THE CODE SNIPPET BELLOW****
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from locale import currency
from pydoc import describe
from proteus import Model, Wizard
from proteus import config as pconfig
import sys
from decimal import Decimal
from datetime import date, datetime, timedelta
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
TODAY = date.today()

def set_config(database, config_file):
    return pconfig.set_trytond(database, config_file=config_file)

def main(database, modules, demo_password, config_file=None):
    config = set_config(database, config_file)
    Module = Model.get('ir.module')
    party_module, = Module.find([('name', '=', 'party')])
    party_module.click('activate')
    Wizard('ir.module.activate_upgrade').execute('upgrade')
    Party = Model.get('party.party')
    Invoice = Model.get('account.invoice')
    Revenue = Model.get('account.journal')
    Position = Model.get('account.invoice.line')
    LinesToPay = Model.get('account.move.line')
    Account = Model.get('account.account')  
    Product = Model.get('product.product') 
    Currency= Model.get('currency.currency')
    Company = Model.get('company.company')
    TaxesName = Model.get('account.tax.template')
    PaymentTerm = Model.get('account.invoice.payment_term')
    revenue, = Revenue.find([('name', '=', 'Revenue')])
    name = "City Association"
    product_name, = Product.find([('name', '=', 'Product1')])
    party, = Party.find([('name', '=', 'City Association')])
    Tax = Model.get('account.invoice.tax')
    TaxName = Model.get('account.tax')
    taxname=TaxName()
    tax_name, = TaxName.find([('name', '=', '19% Umsatzsteuer (ab 2021)')])

    #import the 1st invoice data
    invoice1 = Invoice(journal=revenue,
                    party=party,
                    type='out',
                    invoice_date=date(2022,8,1),
                    description="test our part invoice")
    invoice1.lines.append(Position(type = 'line',
                    product = product_name,
                    quantity = Decimal('1'),
                    unit_price = Decimal('2'))) 
    invoice1.lines.append(Position(type = 'line',
                    product = product_name,
                    quantity = Decimal('4'),
                    unit_price = Decimal('6'))) 
    invoice1.lines.append(Position(type = 'comment',
                    description = "Made a description test"))
    invoice1.lines.append(Position(type = 'line',
                    product = product_name,
                    quantity = Decimal('3'),
                    unit_price = Decimal('2'))) 
    invoice1.lines.append(Position(type = 'comment',
                    description = "Made a description test2"))
    invoice1.save()
    print (invoice1.state) #====>invoice on state 'draft'

    #import the 2nd invoice data
    name2 = "Society Library"
    revenue2, = Revenue.find([('name', '=', 'Revenue')])
    party2, = Party.find([('name', '=', name2)])
    invoice2 = Invoice(journal=revenue2,
                    party=party2,
                    type='out',
                    invoice_date=date(2022,6,5),
                    description="test our  invoice for  Library")   
    invoice2.lines.append(Position(type = 'line',
                    product = product_name,
                    quantity = Decimal('4'),
                    unit_price = Decimal('1'))) 
    invoice2.lines.append(Position(type = 'comment',
                    description = "Testing"))
    invoice2.save()
    invoice2.click('post') 
    print (invoice2.state) #====>invoice posted
    
if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', dest='config_file')
    parser.add_argument('-m', '--module', dest='modules', nargs='+',
        help='module to activate', default=[
            'account',
            'account_invoice',
            'account_payment',
            'company',
            'party',
            'party_avatar',
            'product',
            'production',
            ])
    parser.add_argument('--demo_password', dest='demo_password',
        default='demo', help='demo password')
    parser.add_argument('-d', '--database', dest='database',
        default='demo', help="database name")
    options = parser.parse_args()
    sys.argv = []
    main(options.database, options.modules, options.demo_password,
        config_file=options.config_file)
```
