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
* Python Confuse

## RUNNING LOCALLY

### Configuration
The application configuration has been externalized. It is assumed that the environment specific configuration file is provided by a CI/CD 
pipeline when the image is deployed. Configurations are handled by [Python Confuse Library](https://confuse.readthedocs.io/en/latest/#). 
Python Confuse looks in these operation system locations under the application name:

* macOS: ~/.config/app or ~/Library/Application Support/app
* Other Unix: ~/.config/app and /etc/app
* Windows: %APPDATA%\app where the APPDATA environment variable falls back to %HOME%\AppData\Roaming if undefined

See the full documentation on [Python Confuse search Paths](https://confuse.readthedocs.io/en/latest/#search-paths).

Copy src/ldap3_demo/resource/config_template.yaml to the appropriate search path for your us in a directory named "ldap3_demo" named "config.yaml."
For macOS you could use "~/.config/ldap3_demo/config.yaml." For Windows you could use %APPDATA%\ldap3_demo\config.yaml."

```shell script
# macOS
mkdir ~/.config/ldap3_demo
###  OPTION A, if you need to edit the file for test or local with real passwords, OR... ###
cp $(pwd)/src/ldap3_demo/resources/config_template.yaml ~/.config/ldap3_demo/config.yaml

###  OPTION B, you can use a symbolic link if you only doing unit tests with the mock server and don't require a password  ###
ln -s $(pwd)/src/ldap3_demo/resources/config_template.yaml ~/.config/ldap3_demo/config.yaml

# Linux
mkdir /etc/ldap3_demo
cp ./src/ldap3_demo/resources/config_template.yaml /etc/ldap3_demo/config.yaml
```

### Running tests or Swagger

1) python3 -m venv --copies venv
1) source venv/bin/activate
1) pip install -r app/requirements.txt
1) pip install .
1) make test
1) make run
8) http://localhost:5000/api/doc

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
