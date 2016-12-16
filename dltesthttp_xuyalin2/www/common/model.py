#!/usr/bin/env python
# -*- coding: utf-8 -*-

from www.common.orm import *
from www.common.other import next_id

class User(Model):
    __table__ = 'dl_user.dl_user'

    user_id = StringField(primary_key=True, default=next_id, ddl='varchar(32)')
    user_account = StringField(ddl='varchar(30)')
    user_password = StringField(ddl='varchar(32)')
    user_type = StringField(ddl='varchar(2)')
    user_status = StringField(ddl='varchar(2)', nullable=True)
    user_name = StringField(ddl='varchar(60)', nullable=True)
    user_phone = StringField(ddl='varchar(11)', nullable=True)
    user_phone_status = StringField(ddl='varchar(1)', nullable=True)
    user_email = StringField(ddl='varchar(60)', nullable=True)
    user_sex = StringField(ddl='varchar(1)', nullable=True)
    user_post = StringField(ddl='varchar(60)', nullable=True)
    lock_timestamp = DatetimeField()
    last_login_timestamp = DatetimeField()
    last_login_ip_address = StringField(ddl = 'varchar(15)', nullable=True)
    create_timestamp = DatetimeField()
    create_person = StringField(default='autotest',ddl = 'varchar(32)', nullable=True)
    updated_timestamp = DatetimeField()
    update_person = StringField(default='autotest',ddl = 'varchar(32)', nullable=True)



class AppVersion(Model):
    __table__ = 't_app_version_management'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(32)')
    app_download_address = TextField()
    version = StringField(ddl='varchar(10)')
    is_force_upgrade = StringField(ddl='varchar(1)')
    os_code = StringField(ddl='varchar(10)')
    os_name = StringField(ddl='varchar(100)')
    equipment_code = StringField(ddl='varchar(10)')
    equipment_name = StringField(ddl='varchar(100)')
    created_timestamp = DatetimeField()
    app_type = StringField(ddl='varchar(10)')



class Invoice(Model):
    __table__ = 'dl_biz_invoices'

    invoice_id = StringField(primary_key=True, default=next_id, ddl='varchar(32)')
    user_id = StringField(ddl='varchar(32)')
    invoice_type = StringField(ddl='varchar(10)')
    invoice_header = StringField(ddl='varchar(240)')
    company_name = StringField(ddl='varchar(180)')
    taxpayer_reg_no = StringField(ddl='varchar(20)')
    register_address = StringField(ddl='varchar(420)')
    register_tel = StringField(ddl='varchar(30)')
    deposit_bank = StringField(ddl='varchar(60)')
    account_bank = StringField(ddl='varchar(32)')
    account_licence = StringField(ddl='varchar(400)')
    receive_man_name = StringField(ddl='varchar(60)')
    receive_man_tel = StringField(ddl='varchar(11)')
    receive_man_province = StringField(ddl='varchar(10)')
    receive_man_address = StringField(ddl='varchar(240)')
    is_default = StringField(ddl='varchar(1)')
    created_timestamp = DatetimeField()
    created_person = StringField(default='autotest',ddl='varchar(32)')
    updated_timestamp = DatetimeField()
    updated_person = StringField(default='autotest',ddl='varchar(32)')


class Shoppingcart(Model):
    __table__ = 'dl_shoppingcart'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(32)')
    user_id = StringField(ddl='varchar(32)')
    goods_id = StringField(ddl='varchar(32)')
    goods_name = StringField(ddl='varchar(240)')
    goods_pic_url = StringField(ddl='varchar(400)')
    unit_price = IntegerField(ddl='int(15)')
    spec_name = StringField(ddl='varchar(32)')
    goods_quantity = IntegerField(ddl='int(11)')
    business_id = StringField(ddl='varchar(32)')
    business_name = StringField(ddl='varchar(180)')
    store_id = StringField(ddl='varchar(32)')
    store_name = StringField(ddl='varchar(240)')
    is_delete = StringField(ddl='varchar(1)')
    created_timestamp = DatetimeField()
    created_person = StringField(default='autotest',ddl='varchar(32)')
    updated_timestamp = DatetimeField()
    updated_person = StringField(default='autotest',ddl='varchar(32)')