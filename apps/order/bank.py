# from azbankgateways import bankfactories, models as bank_models
#
#
# def bank_verify():
#     factory = bankfactories.BankFactory()
#
#     # غیر فعال کردن رکورد های قدیمی
#     bank_models.Bank.objects.update_expire_records()
#
#     # مشخص کردن رکوردهایی که باید تعیین وضعیت شوند
#     for item in bank_models.Bank.objects.filter_return_from_bank():
#         bank = factory.create(bank_type=item.bank_type, identifier=item.bank_choose_identifier)
#         bank.verify(item.tracking_code)
#         bank_record = bank_models.Bank.objects.get(tracking_code=item.tracking_code)
#         if bank_record.is_success:
#             pass
#         else:
#             print('None')
