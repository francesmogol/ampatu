Ampatu is a 911 Emergency Event Management web application running on top of the web2py Python framework and PostgreSQL database.

Goals:

  * Easy to use
  * Simple and customizable design
  * Minimal maintenance
  * Low cost & commodity hardware support
  * Free software (open source) based on volunteer collaboration

Features:

  * Incident archiving: event type, reporting party, telephone transcript synopsis, phone/911/radio operator and custom data (for Fire, Police & Emergency Medical Services, et.al.)
  * Simple 4 state tray-like workflow:
    * Red: pending
    * Yellow: dispatched
    * Blue: on site
    * Green: closed
  * Single or Multiple Unit/Team assignation per incident
  * Zone (Grid), Station, District, Emergency Agency grouping
  * Time-stamping, logging and comments
  * Statistical Reports and Crime-Map generation
  * GIS (using PostgreSQL geometric types and funcions):
    * Adress lookup and normalization (if Street Guide/Map available)
    * Mobile unit location/tracking (if AVL available)

Current development is a migration of an earlier GUI project based on a Visual Basic front-end / PostgreSQL back-end, successfully used in several Buenos Aires (Argentina) police stations, winner of the [Award for Innovation in Public Administration 2008](http://www.dpgp.sg.gba.gov.ar/html/premio2008/premio2008_ganadores.pdf) (Premio a la Innovación en la Gestión Pública 2008: "Sistema de Gestión de Eventos de Emergencias 911")

This project was also developed as Academic Field Work
  * [Initial Doc](https://docs.google.com/fileview?id=0B__UYqYT4LNaY2I0OTBkOTQtNzIyYi00MWMwLWEzMjAtNzViZWM4ZGU2NzE5&hl=en) describing project scope, requeriments and analysis (UML use cases, class and state diagram, tentative screens and navigation map)
  * [Final Doc](https://docs.google.com/fileview?id=0B__UYqYT4LNaMzI5OGNiOTMtYzg5Ni00Mzk0LThmZmMtYTA3ZTdlNmZmMTc4&hl=en) describing implementation details (UML diagrams and modifications)

See on downloads for a legacy system implemented in VB, the academic one implemented in PHP.

For further information, contact reingart@gmail.com