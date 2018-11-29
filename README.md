# Accio

## Work In Progress
This project is still work in progress, some features may be not implemented yet or works differently than described in documentation. In fact documentation is more like a specification I follow to implement features, but a lot of things changed.

To fully understand what this project is about I suggest to visit another repository in https://github.com/g1ntas/ex-accio

If you want to run and mess around with this project you can use templates I use for testing in repository github.com/g1ntas/accio-templates. They most likely will be up-to date.

## Requirements
1. Python 3.6+
2. Git client command line executable

## Repository structure
TODO

## Commands
### > accio repo add {git_repository_url}
Clones repository, identifies all defined generators by reading config files and caches them for future use.

*NOTE:* if authentication is required, git executable deals with it.

### > accio repo list
Lists all added repositories with corresponding indexes

e.g.
```
> [0] github.com/example/repository1
> [1] github.com/example/repository2
> [2] gitlab.com/example/repository3
```

### > accio repo remove {index}
Removes repositories by given index(-es). Prompts for confirmation. 

Options/flags:
```
--all                  Removes all repositories
-f, --force            Don't ask for confirmation
```

### > accio repo sync
Updates/syncs all repositories (pulls changes).

Options/flags:
```
-r, --repo [int,...]  Index of specific repository to sync with
```

### > accio run [generator]
Looks up for the given generator name in imported repositories. If found, prompts for required input defined in config and renders  templates at cwd.

If path for any of templates is already taken, prompts for confirmation to overwrite.

If multiple occurrences have been found of given generator name, then prompts to choose only one:
```
> accio run example
> Multiple generators of `generator:example` have been found:
> [0] {description of command} (github.com/example/repo1)
> [1] {description of command} (github.com/example/repo2)
Enter which one to run: 
``` 

Options/flags:
```
-f, --force  Existing paths are overwritten.
-h, --help   Prints help text from generator's config
-w, --working-dir [dir]  Specify different working dir than current one
```


### accio list
Lists all existing generators with descriptions (taken from configs).

## Config reference
Every generator must have config named `accio.yaml`

### description `required`
Short description of command (up to 120 chars) used to list available generators.

e.g. `description: 'It is a short description of generator'`

### help `optional`
Description which will be showed when `—help` option is provided for specific generator.

*NOTE:* `—help` flag will already include description as a first paragraph, so this option should be used for more verbose explanation of generator. 

e.g. `help: 'It is a help text with unlimited amout of characters'`

### prompts `optional`
Map that contains definitions of variables that will be prompted when generator is ran. Variables will be accessible globally in scripts and templates.

Each definition has these options:

#### type `required`
Type of input:

`int`
`float`
`bool`
`string`
`list:{int, bool, float, string}`

#### description `optional`
Description of argument used for help

e.g.
```
variables:
  var1:
	  type: int # required
	  description: 'Short help text' # optional
  var2: { type: list:string }
```

### Full example:
```
name: 'accio:example'
description 'Description text'
help: 'Help text'
variables:
  var1:
	  type: int # required
	  description: 'Short help text' # optional
  var2: { type: list:string }
scripts:
  - scripts/example1.ank
  - scripts/example2.ank
templates:
  - templates/example1.mustache
  - templates/example2.mustache
```

## Templates
Accio templates are combination of python scripts and mustache templates, that are separated as front matter:

e.g.
```

---
first_name = "Lorem"
last_name = "Ipsum"
name = "{0} {1}".format(first_name, last_name)

ctx.set_variable("full_name", name)
---

Hello, {{full_name}}
```

## Scripts
Scripts are run in python sandbox

### Context
All communication between scripts and templates are done by context (`ctx` object).

There are 2 scopes of contexts, global and individual.

Global context is initialised at the start of program and can be accessed and modified only in global scripts. All prompted variables are also set in global context. 

Individual context are initialised for each template and contains everything global contexts has (variables, functions), but changes to context are applied only for that template.

#### Context API
`context.Vars` 
Contains structure of variables

`context.Vars.set(name, value)` 
Sets new variable. If it’s already defined, it can be overwritten, but only if new value is the same type as the old one.

`context.Vars.unset(name)` 
Unsets context variable.

`context.Vars.get(string name) ({}interface, exists)`
Returns value of context variable.

TODO: need to rethink how to handle different variable types

`context.Functions.set(reference)`


`context.Settings.set(name)`

#### Context settings

`path`  - override path of current template (by default it is path to current file)

`ignore` - if `true` current template will not be generated (default: `false`)

