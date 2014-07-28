# odooenv
Tool to administrate Odoo environments

Moldeo Interactive (c) 2014-2018
 Cristian S. Rocha
 csr@moldeo.coop

This code is distributed under the MIT license.

## Instroduction

OdooEnv is a python based environment manager. It's come from OERPenv which exists in "https://launchpad.net/oerpenv". But when renamed OpenERP to Odoo, whe change the name and repository plase.

## Requirements

Using PIP installer.

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
	  -h, --help            show this help message and exit

	subcommands:
	  The Odoo environment administrator help you to administrate Odoo
	  environments. You can use the following commands.

	  {init,update,create,add,install,list-installables,list-addons,enable,disable,dummy,test,client,search,show}
				commands
	    init                Init an environment in the work path or in the
				declared path.
	    update              Update sources.
	    create              Create a new python environment.
	    add                 Add a branch with to the sources list.
	    install             Install all software in the default environment of in
				the declared.
	    list-installables   List all availables applications in sources.
	    list-addons         List availables addons in sources. Show all addons if
				not filter expression declared.
	    enable              Enabel addons on the environment. Create a symbolic
				link.
	    disable             Disable addons on the environment. Remove a symbolic
				link.
	    dummy               Create a dummy addon. Useful to create new addon.
	    test                Execute the server in test mode for this addon.
	    client              Execute the server in test mode for this addon.
	    search              Search addon with this object.
	    show                Show addon information.
```
   

All configurations are stored in the environment.conf file. You can setup it by hand or by using the available commands listed above.

## Testing a module:

To create a simple Odoo instance you need to run the following commands in your work directory.

```
$ odooenv init odoo_env
$ cd odoo_env
$ odooenv update
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

In the output you can find the source path. There you can found the __odoo__.py file. Append the modules you want to test in the 'depends' field, in this example will use hr_attendace and hr_contract. If you done all right you can execute the follwing command without errors:

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

