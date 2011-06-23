~~~~~~~~~~~~~
dynamicschema
~~~~~~~~~~~~~

This example demonstrates how one can use a EAV (Entity Attribute Value) approach in django to create schemas and perform CRUD operations on the added schema without altering the tables. This design is very helpful when we have to add different record types frequenty. 

$ manage.py syncdb
- Create an admin account, it is needed to create the schema.

$ manage.py runserver

visit http://localhost:8000/cck/ListSchemas/

~~~~~~~
License
~~~~~~~
dynamicschema is License under the terms of BSD License. Please read the
contents of the LICENSE file in the root of the source repository for the
terms of the license.

~~~~~~~
Authors
~~~~~~~
The authors and/or contributors of dynamicschema is listed in the AUTHORS
file in the root of the source repository.
