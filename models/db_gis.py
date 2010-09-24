# coding: utf8

#
# GIS for address lookup
# ----------------------

db.define_table('street',
    Field('id', 'id'),
    Field('name', 'string', length=250, unique=True),
    migrate=migrate)

db.define_table('street_map',
    Field('id', 'id'),
    Field('street_id', 'integer'),
    Field('house_number_from', 'integer'),
    Field('house_number_to', 'integer'),
    Field('city', 'string', length=50),
    Field('label', 'string', length=250),
    Field('segment', 'text'),
    migrate=migrate)
