# LDAP3 Demo

This is generic wrapper for LDAP3. I am looking at whether a generic template could be used for
OpenLDAP, Active Directory, Novell, etc where the only difference was logic to discover
and manage servers. The other reason for separating the microservices by backing service
would be to use vendor specific LDAP extensions.

A core principle of this POC is one microservice per LDAP backing service. Of course, this
could be done in a single LDAP microservice, but that would increase the complexity. 
Also, you could argue it would infringe on The Twelve Factors because deploying a bug fix 
for Active Directory could affect OpenLdap services too. 

## TECHNOLOGIES
This project uses the following libraries.
* Flask
* Ldap3
* Marshmallow
* Pytest
* Swagger

## RUNNING LOCALLY

1) python3 -m venv --copies venv
2) source venv/bin/activate
3) pip install -r app/requirements.txt
4) pip install .
5) make test
6) make run
7: http://localhost:5000/api/doc

# RESOURCES
These are the references I used in structuring this project. Full disclosure, I wrote Java
for 20 years, so you won't find a models.py file. I give every class its own file and
it's own test file.

I started with [Martin Heinz's](https://martinheinz.dev/) project blueprint, folded in ideas from 
[Sean Bradley's](https://github.com/Sean-Bradley) Flask Rest boilerplate, and then I refactored the project test packaging 
as proposed by [Ionel Cristian Mărieș](https://blog.ionelmc.ro/about/).

* https://github.com/ionelmc/cookiecutter-pylibrary
* https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
* https://towardsdatascience.com/ultimate-setup-for-your-next-python-project-179bda8a7c2c
* https://github.com/Sean-Bradley/Seans-Python3-Flask-Rest-Boilerplate
* https://github.com/MartinHeinz/python-project-blueprint
