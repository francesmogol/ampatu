# coding: utf8
# intente algo como
def index(): return dict(message="incidents main page")

@auth.requires_login()
def create(): 
    form = SQLFORM(db.incident,
        fields=['contact', 'event_id', 'location', 'phone', 'reported_by', 
                  'synopsis', 'started_at', 'severity'])
    # check submited form (custom insert if ok)
    if form.accepts(request.vars, session, dbio=False):
        incident_id = db.incident.insert(**form.vars)
        response.flash = T("Incident %s created!") % incident_id
    elif form.errors:
        response.flash = T("Incident not saved! (correct errors!)") 
    else:
        response.flash = T("Complete the form") 
    return dict(form=form)

@auth.requires_login()
def monitor():
    def list_incidents(status,link_fn):
        query = db.incident.status==status
        fields = (db.incident.id, db.incident.started_at, db.incident.event_id)
        rows = db(query).select(*fields)

        return SQLTABLE(rows, headers={'incident.id': T('Id'), 
                                           'incident.started_at': T('Started at'), 
                                           'incident.event_id': T('Event')},
                             linkto=lambda field, type, ref: URL(r=request, f=link_fn, args=[field]),)
                             
    
    # incoming incidents
    red_table = list_incidents(status='R', link_fn='assign')
    
    # dispatched incidents
    yellow_table = list_incidents(status='Y', link_fn='update')

    # arrived on-scene
    blue_table = list_incidents(status='B', link_fn='close')                             
        
    return dict(red_table=red_table, yellow_table=yellow_table, blue_table=blue_table)


@auth.requires_login()
def assign():
    if not request.args:
        session.flash = T("Invalid incident!")
        redirect(URL("monitor"))
    incident_id = request.args[0]
    incident = db.incident(incident_id)

    # show gmap api...
    # get available units (near)
    rows = db(db.unit.available==True).select(db.unit.id, db.unit.description)
    available_units = dict([(row.id, row.description) for row in rows]) 
    
    form=SQLFORM.factory( 
         Field('location', 'string', label=T("Location"), 
             default=incident.location, writable=False),
         Field('reported_by', 'string', label=T("Reported by"), 
             default=incident.reported_by, writable=False),
         Field('synopsis', 'text', label=T("Synopsis"), 
             default=incident.synopsis, writable=False),
         Field('unit_id',  label=T("Assign unit"),
             requires=IS_IN_SET(available_units)),
         )
         
    if form.accepts(request.vars, session):
        db(db.incident.id==incident_id).update(unit_id=form.vars.unit_id, status="Y")
        db(db.unit.id==form.vars.unit_id).update(available=False)
        redirect(URL(r=request, f="monitor"))
    return dict(form=form)


@auth.requires_login()
def update(): 
    if not request.args:
        session.flash = T("Invalid incident!")
        redirect(URL("monitor"))
    incident_id = request.args[0]
    
    form = SQLFORM(db.incident, incident_id,
        fields=['contact', 'event_id', 'location', 'phone', 'reported_by', 'synopsis', 'started_at', 'severity'],
        readonly=True)
    # check submited form (custom insert if ok)
    if form.accepts(request.vars, session, dbio=False):
        incident_id = db.incident.insert(**form.vars)
        response.flash = T("Incident %s created!") % incident_id
    elif form.errors:
        response.flash = T("Incident not saved! (correct errors!)") 
    else:
        response.flash = T("Complete the form") 
    return dict(form=form)


def busqueda():

    form=SQLFORM.factory( 
         Field('texto', 'string', default='', writable=True),
         
         )

    if form.accepts(request.vars, session):
        query = db.incident.location.contains(form.vars.texto)
        filas = db(query).select()
    else:
        filas = []
        
    return dict(resultado=filas, form=form)
