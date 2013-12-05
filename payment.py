## coding: utf-8
# This file is part of account_payment_es_csb_34_01 module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
import logging
try:
    from retrofix import Record, write, c34_01
except ImportError:
    message = ('Unable to import retrofix library.\n'
               'Please install it before install this module.')
    logging.getLogger('account_payment_es_csb_34_01').error(message)
    raise Exception(message)

__all__ = [
    'Journal',
    'Group',
    ]
__metaclass__ = PoolMeta


class Journal:
    __name__ = 'account.payment.journal'

    @classmethod
    def __setup__(cls):
        super(Journal, cls).__setup__()
        if ('csb34_01', 'CSB 34-01') not in cls.process_method.selection:
            cls.process_method.selection.extend([
                ('csb34_01', 'CSB 34-01'),
                ])


class Group:
    __name__ = 'account.payment.group'

    @classmethod
    def __setup__(cls):
        super(Group, cls).__setup__()
        cls._error_messages.update({
            'company_without_complete_address': ('The company %s has no a '
                'complete address to add to the file.'),
            'party_without_address': ('The party %s has no an address to add '
                'to the file.'),
            'party_without_complete_address': ('The party %s has no a country '
                'neither a state in its address.'),
            'party_without_vat_number': ('The party %s has no any vat '
                'number.'),
            })

    def set_default_csb34_01_payment_values(self):
        values = self.set_default_csb34_payment_values()
        # Set company address values

        # TODO: For the time, the charge_detail is only implemented for
        # 'with_relationship'
        values['with_relationship'] = 'with_relationship'
        # TODO: For the time, the expenses are only implemented for
        # 'expenses_by_payer'
        values['expenses_by_payer'] = 'expenses_by_payer'
        # TODO: For the time, set_header_record_process_method_5 and
        # set_header_record_process_method_6 are optional, so are not
        # implemented
        for receipt in values['receipts']:
            # TODO: For the time, the operation code is only implemented for
            # transfers
            receipt['operation_code'] = 'transfer'
            # TODO: For the time, the another identifier document is not
            # implemented
            receipt['another_id_doc'] = ''
        values['record_count'] = 0
        values['payment_count'] = 0
        return values

    @classmethod
    def process_csb34_01(cls, group):
        def set_header_record_process_method_1():
            record = Record(c34_01.HEADER_RECORD_TYPE_1)
            record.record_code = '03'
            record.operation_code = '56'
            record.nif = values['vat_number']
            record.notebook_version = '34016'
            record.data_number = '001'
            record.send_date = values['creation_date']
            record.creation_date = values['payment_date']
            record.bank_code = values['bank_account'][0:4]
            record.bank_office = values['bank_account'][4:8]
            record.bank_account_num = values['bank_account'][10:20]
            record.charge_detail = values['with_relationship']
            record.expenses = values['expenses_by_payer']
            record.bank_account_dc = values['bank_account'][8:10]
            return write([record])

        def set_header_record_process_method_2():
            record = Record(c34_01.HEADER_RECORD_TYPE_2)
            record.record_code = '03'
            record.operation_code = '56'
            record.nif = values['vat_number']
            record.data_number = '002'
            record.name = values['name']
            return write([record])

        def set_header_record_process_method_3():
            record = Record(c34_01.HEADER_RECORD_TYPE_3)
            record.record_code = '03'
            record.operation_code = '56'
            record.nif = values['vat_number']
            record.data_number = '003'
            record.address = values['street']
            return write([record])

        def set_header_record_process_method_4():
            record = Record(c34_01.HEADER_RECORD_TYPE_4)
            record.record_code = '03'
            record.operation_code = '56'
            record.nif = values['vat_number']
            record.data_number = '004'
            record.city = values['city']
            return write([record])

        def set_recipient_record_process_method_1():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_1)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '010'
            record.amount = receipt['amount']
            record.bank_code = receipt['bank_account'][0:4]
            record.bank_office = receipt['bank_account'][4:8]
            record.bank_account_num = receipt['bank_account'][10:20]
            record.concept = 'others'
            record.bank_account_dc = receipt['bank_account'][8:10]
            return write([record])

        def set_recipient_record_process_method_2():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_2)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '011'
            record.name = receipt['name']
            return write([record])

        def set_recipient_record_process_method_3():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_3)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '012'
            record.address = receipt['street']
            return write([record])

        def set_recipient_record_TYPE_4():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_4)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '013'
            record.address2 = receipt['street2']
            return write([record])

        def set_recipient_record_process_method_5():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_5)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '014'
            record.zip_city = receipt['zip_city']
            return write([record])

        def set_recipient_record_process_method_6():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_6)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '015'
            record.province = receipt['province']
            return write([record])

        def set_recipient_record_process_method_7():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_7)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '016'
            record.concept = receipt['concept']
            return write([record])

        def set_recipient_record_process_method_8():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_8)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '011'
            record.concept2 = receipt['concept2']
            return write([record])

        def set_recipient_record_process_method_9():
            record = Record(c34_01.RECIPIENT_RECORD_TYPE_9)
            record.record_code = '06'
            record.operation_code = receipt['operation_code']
            record.nif = values['vat_number']
            record.recipient_nif = receipt['vat_number']
            record.data_number = '011'
            record.beneficiary_nif = receipt['vat_number']
            record.another_id_doc = receipt['another_id_doc']
            return write([record])

        def set_record_of_totals():
            record = Record(c34_01.RECORD_OF_TOTALS)
            record.record_code = '08'
            record.operation_code = '56'
            record.nif = values['vat_number']
            record.amount = values['amount']
            record.payment_line_count = str(values['payment_count'])
            record.record_count = str(values['record_count'])
            return write([record])

        values = Group.set_default_csb34_01_payment_values(group)
        text = set_header_record_process_method_1()
        values['record_count'] += 1
        text += set_header_record_process_method_2()
        values['record_count'] += 1
        text += set_header_record_process_method_3()
        values['record_count'] += 1
        text += set_header_record_process_method_4()
        values['record_count'] += 1
        for receipt in values['receipts']:
            text += set_recipient_record_process_method_1()
            values['record_count'] += 1
            text += set_recipient_record_process_method_2()
            values['record_count'] += 1
            values['payment_count'] += 1
        values['record_count'] += 2
        text += set_record_of_totals()
        group.attach_file(text)
