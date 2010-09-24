# coding: utf8

migrate=True

# police, fire dept, medical emergency, civil (emergency service departments)
db.define_table('agency', 
    Field('id', 'id'),
    Field('name', 'string'),
    format=lambda a: a.name,
    )

db.define_table('district',
    Field('id', 'id'),
    Field('name', 'string', length=250),
    format=lambda d: d.name,
    migrate=migrate)
    
db.define_table('station',
    Field('id', 'id'),
    Field('code', 'string', length=5, unique=True),
    Field('name', 'string', length=50),
    Field('distrit_id', 'reference district'),
    Field('address', 'text'),
    Field('phone', 'text'),
    format=lambda s: s.name,
    migrate=migrate)

db.define_table('zone', # grid (cuadricula)
    Field('id', 'id'),
    Field('code', 'string', length=5, unique=True),
    Field('station_id', db.station),
    Field('city', 'string', length=250), # localidad
    Field('county', 'string', length=250), # partido
    Field('limits', ), #polygon, unssuported by now
    format=lambda z: z.code,
    migrate=migrate)

db.define_table('unit',
    Field('id', 'id'),
    Field('description', 'string', length=250),
    Field('code', 'string', unique=True),
    Field('updated_at', 'datetime'),
    Field('latitude', 'double' ),
    Field('longitude', 'double' ),
    Field('available', 'boolean', default=True),
    format=lambda u: u.description,
    migrate=migrate)

db.define_table('person',
    Field('id', 'id'), # legajo
    Field('name', 'string', length=250),
    Field('code', 'string', unique=True),    
    Field('skills', 'text'),
    format=lambda p: p.name,
    migrate=migrate)

db.define_table('team', # movil_operativo
    Field('id', 'id'),
    Field('unit_id', 'reference unit'),
    Field('leader_id', 'reference person'), # A/C
    Field('zone_id', 'reference zone'), # pre-assigned zone
    Field('formed_by', 'datetime', default=request.now), # alta
    Field('formed_until', 'datetime'),  # baja
    Field('available', 'boolean'),
    migrate=migrate)

# Incident Types: assault, steals, robbery, fire, car crash, trauma, heart attack, choking, etc.
db.define_table('event',
    Field('id', 'id'),
    Field('name', 'string', length=50),
    Field('category', 'string'), 
    Field('nature', 'string', requires=IS_IN_SET(["life", "health", "property"])), # 
    format=lambda e: e.name,
    migrate=migrate)

# 911 Calls
db.define_table('incident',
    Field('id', 'id'),
    # Initial data (red status):
    Field('contact', 'string', label=T("Contact"),
        comment=T("911 Operator (calltaker)"), ), # op911     
    Field('event_id', db.event, label=T("Event"),
        comment=T("Incident Type"),),
    Field('location', 'string', label=T("Location"),
        comment=T("Street name, house number, direction (if any)"), ), # ubicación
    Field('phone', 'string', label=T("Phone"), # telefono
        comment=T("Source telephone number")), 
    Field('reported_by', 'string', label=T("Reported by"), 
        comment=T("Calling party name")),  # denunciante
    Field('synopsis', 'text', label=T("Synopsis"),
        comment=T("Actual Phone Transcript")),   # novedad telefónica
    Field('started_at', 'datetime', label=T("Started at"),
        comment=T("Start date & time"),
        default=request.now), # fecha y hora de inicio
    Field('created_by', db.auth_user, label=T("Created by"),
        default=auth.user_id, 
        comment=T("Phone Operator")), # optel
    Field('severity', 'string', length=1, label=T("Severity"),
        comment=T("Priority classification"), 
        requires=IS_IN_SET(["A", "B", "C", "D"])),
    Field('status', 'string', length=1, label=T("Status"),
        requires=IS_IN_SET({'R':'Red','Y':'Yellow','B':'Blue', 'G':'Green'}), 
        default='R'),
    # Dispatch (responding) data (yellow status):
    Field('unit_id', db.unit, label=T("Unit"),
        comment=T("Main unit assigned")),
    Field('dispatched_by', db.auth_user, label=T("Dispatched by"),), #opradio
    Field('dispatched_at', 'datetime', label=T("Dispatched at"),
        comment=T("Dispatch date & time")), # hora_intervencion
    Field('latitude', 'double'),
    Field('longitude', 'double'),
    Field('zone_id', db.zone, required=False, label=T("Zone"),), # cuadricula
    Field('comments', 'text', label=T("Comments"),
        comment=T("Action, scope, etc."), ), # novedad real
    # Closing (on scene) data (blue/green status):
    Field('arrived_at', 'datetime', label=T("Arrived at"),
        comment=T("On scence date & time")), # hora_intervencion
    Field('contacted', 'string', length=1), # entrevistado
    Field('delay', 'double', label=T("Delay"), 
        comment=T("Delay in seconds (calculated)"), # demora (calculada)
        compute=lambda i: 'arrived_at' in i and (i['arrived_at']-i['started_at'])), 
    Field('confirmed', 'boolean', label=T("Confirmed"), ),
    Field('preventable', 'boolean', label=T("Preventable"), ),
    Field('relevant', 'boolean', label=T("Relevant"), ),
    Field('medical', 'boolean', label=T("Medical"), ),
    Field('updated_at', 'datetime', label=T("Updated at"),
        comment=T("Last modification date & time"),
        update=request.now, writable=False),
    # Custom data (blue/green status):
    Field('arrested_adult', 'integer', label=T("Arrested Adult"),),
    Field('arrested_minor', 'integer', label=T("Arrested Minor"),),
    Field('seized_vehicles', 'integer', label=T("Seized Vehicles"),),
    Field('seized_weapons', 'integer', label=T("Seized Weapons"),),
    Field('seized_drugs', 'integer', label=T("Seized Drugs"),),
    migrate=migrate)

db.define_table("assignment",
    Field('incident_id', db.unit),
    Field('unit_id', db.unit),
    Field('team_id', db.team),
    Field('assigned_by', db.auth_user),
    Field('assigned_at', 'datetime', default=request.now),
    migrate=migrate)
