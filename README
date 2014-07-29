# odooenv
Tool to administrate Odoo environments

Moldeo Interactive (c) 2014-2018
 Cristian S. Rocha
 csr@moldeo.coop

This code is distributed under the MIT license.

## Introduction

OdooEnv is a python based environment manager. It is a derivative from OERPenv which exists in "https://launchpad.net/oerpenv". But when OpenERP was renamed to Odoo, we changed the OERPEnv to OdooEnv. We also changed the source repository, changing it from launchpad to github.

## Installation

Using PIP installer (pip needs to be installed)

```
 pip install odooenv
```

## Usage:

The odooenv command line is available with the following sub-commands:


```
	usage: odooenv [-h]
		       
		       {init,update,create,add,install,list-installables,list-addons,enable,disable,dummy,test,client,search,show}
		       ...

	optional arguments:
	  -h, --help            shows this help message and exits

	subcommands:
	  The Odoo environment administrator helps you administrate Odoo
	  environments. You can use the following commands.

	  {init,update,create,add,install,list-installables,list-addons,enable,disable,dummy,test,client,search,show}
				commands
	    init                Initializes an environment in the work path or in the
				declared path.
	    update              Updates sources.
	    create              Creates a new python environment.
	    add                 Adds a branch to the sources list.
	    install             Installs all the required software in the default environment. The packages to be installed need to be declared 
				in the environment file. 
	    list-installables   Lists all available applications in sources.
	    list-addons         Lists available addons in sources. Shows all addons if
				not filter expression declared.
	    enable              Enables addons on the environment. Creates a symbolic
				link.
	    disable             Disables addons on the environment. Removes a symbolic
				link.
	    dummy               Creates a dummy addon. Useful for creating a new addon from scratch.
	    test                Executes the server in test mode for this addon.
	    client              Executes the server in test mode for this addon.
	    search              Searchs addon with this object.
	    show                Shows addon information.
```
   

All configurations are stored in the environment.conf file. You can setup it by hand or by using the available commands listed above.

## Testing a module:

To create a simple Odoo instance you need to run the following commands in your work directory.

```
$ odooenv init odoo_env
$ cd odoo_env
$ odooenv install
$ odooenv list-addons
```

Search for an addon to test, like hr_attendance

```
$ odooenv enable hr_attendance
$ odooenv test hr_attendance
```

In case you want to run the server, you only need to execute:

```
$ odooenv server-start --debug
```

The server should be running and you can start working with Odoo by launching your browser and pointing it to the appropiate port (commonly 8069)

## Develop a new addon not from zero:

If you need test more than one module, or you want develop a new addon you can create a dummy addon in the following way:

```
$ odooenv dummy hr_test
```

In the output you can find the source path. There you can found the __openerp__.py file. Append the modules you want to test in the 'depends' field, in this example will use hr_attendace and hr_contract. If you done all right you can execute the follwing command without errors:

```
$ odooenv enable hr_test
```

Then you can execute the server in mode test again, for the new module.

```
$ odooenv test hr_test
```

# Searching for an object in source code:

To search the source code of a code you can use the command 'search'.

# Display addon information:

To show addon information, like description, declarated objects and path to the source you can use the command 'show'.

