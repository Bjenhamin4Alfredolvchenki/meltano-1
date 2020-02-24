---
metaTitle: Using the Meltano CLI
description: The Meltano command line interface makes it easy to develop, run, and debug every step of the data analysis lifecycle.
sidebarDepth: 2
---

# Command Line Interface

Meltano provides a command line interface (CLI) that allows you to manage the configuration and orchestration of Meltano instances. It provides a single source of truth for the entire data pipeline. The CLI makes it easy to develop, run, and debug every step of the data life cycle.

- [Getting Started Guide for the Command Line](#getting-started-with-meltano-on-the-command-line)
- [Glossary of Command Line Concepts](#glossary-of-command-line-concepts)

## Getting Started with Meltano on the Command Line

Once you have successfully installed Meltano from the command line, you will need to create a project before you launch the Meltano UI.

## Create your first project

To initialize a new project, open your terminal and navigate to the directory that you'd like to store your Meltano projects in.

Use the `meltano init` command, which takes a `PROJECT_NAME` that is of your own choosing. For this guide, let's create a project called "myprojectname".

```bash
meltano init myprojectname
```

This will create a new directory named `myprojectname` in the current directory and initialize Meltano's basic directory structure inside it.

Inside the Meltano project directory, all plugin configuration (which may include tokens and passwords) is stored inside the `.meltano` directory, which is automatically added to the project's `.gitignore` file to prevent this potentially sensitive information from accidentally being pushed up to a hosted Git repository.

## Setup your loader

Self-hosted Meltano instances require you to configure your reporting database, which we call the Meltano **Loader**, from the command line. To do this, you will supply your database configuration through a `.env` file.

Once you create the file, you will need to paste in the configuration for your database. For example, PostgreSQL configurations can [be found here](/plugins/loaders/postgres.html#intermediate-connecting-meltano-to-an-existing-postgresql-database).

After saving your configurations, you can load your configurations by running:

```bash
source .env
```

And just like that, your loader is configured!

## Start the application

Now that you've created your first Meltano project, let's change directory to our new project and start Meltano UI:

```bash
cd myprojectname
meltano ui
```

Meltano is now running and should open a new tab at [http://localhost:5000](http://localhost:5000).

Now that you have access to the Meltano UI, [use our Getting Started guide](http://localhost:8080/docs/getting-started.html#create-your-meltano-account) to learn more about how to use the software.


## Glossary of Command Line Concepts

## `add`

The `add` command allows you to add an extractor, loader, or transform to your Meltano instance.

### Extractor / Loader

When you add a extractor or loader to a Meltano instance, Meltano will:

1. Add it to the `meltano.yml` file
1. Installs it in the `.meltano` directory with `venv` and `pip`

You can run `meltano add` with `--include-related` to automatically install all transform, model, and dashboard plugins related to an extractor.

#### Examples

```bash
# Extractor / Loader Template
meltano add [extractor | loader] [name_of_plugin]

# Extractor Example
meltano add extractor tap-gitlab

# Extractor Example including related plugins
meltano add --include-related extractor tap-google-analytics

# Loader Example
meltano add loader target-postgres
```

### Transform

When you add a transform to a Meltano instance, Meltano will:

1. Installs dbt transformer to enable transformations (if needed)
1. Add transform to `meltano.yml file`
1. Updates the dbt packages and project configuration

#### Example

```bash
# Transform Template
meltano add [transform] [name_of_transform]
```

### Model

When you add a model to a Meltano instance, Meltano will:

1. Add a model bundle to your `meltano.yml` file to help you interactively generate SQL
1. Install the model inside the `.meltano` directory which are then available to use in the Meltano webapp

#### Example

```bash
meltano add model [name_of_model]
```

### Dashboard

When you add a dashboard to a Meltano instance, Meltano will:

1. Add a dashboard bundle to your `meltano.yml` file
1. Install the dashboard and reports inside the `analyze` directory which are then available to use in the Meltano webapp

#### Example

```bash
meltano add dashboard [name_of_dashboard]
```

### Orchestration

When you add an orchestrator to a Meltano instance, Meltano will:

1. Adds an orchestrator plugin to your **meltano.yml**
1. Installs it

#### Example

```bash
meltano add orchestrator [name_of_orchestrator]
```

## `config`

Enables you to change a plugin's configuration.

Meltano uses configuration layers to resolve a plugin's configuration:

1. Environment variables
1. Plugin definition's `config:` attribute in **meltano.yml**
1. Settings set via `meltano config` or in the UI (stored in the system database)
1. Default values set in the setting definition in **discovery.yml**

::: info
Sensitive settings such as _passwords_ or _keys_ should not be configured using `meltano.yml`, 
since the entire contents of this file are available to the Meltano UI and its users.

Instead, these sensitive values should be stored in environment variables, or the system database (using `meltano config` or the UI).

You can use `meltano config <plugin_name> list` to find the environment variable associated with a setting.

Note that in each of these cases, Meltano stores the configuration as-is, without encryption.
:::

### How to use

```bash
# Displays the plugin's configuration.
meltano config <plugin_name>

# List the available settings for the plugin.
meltano config <plugin_name> list

# Sets the configuration's setting `<name>` to `<value>`.
meltano config <plugin_name> set <name> <value>

# Remove the configuration's setting `<name>`.
meltano config <plugin_name> unset <name>

# Clear the configuration (back to defaults).
meltano config <plugin_name> reset
```

## `discover`

Lists the available plugins you are interested in.

### How to Use

```bash
# List all available plugins
meltano discover all

# Only list available extractors
meltano discover extractors

# Only list available loaders
meltano discover loaders

# Only list available models
meltano discover models
```

## `elt`

This allows you to run your ELT pipeline to Extract, Load, and Transform the data with configurations of your choosing:

1. The `job_id` is autogenerated using the current date and time if it is not provided (via `--job_id` or `$MELTANO_JOB_ID`)
1. The `run_id` is a UUID autogenerated at each run
1. All the output generated by this command is also logged in `.meltano/run/elt/{job_id}/{run_id}/elt.log`

### How to use

```bash
meltano elt <extractor> <loader> [--job_id TEXT] [--transform run] [--dry]
```

### Parameters

- The `--transform` option can be:

  - `run`: run the Transforms
  - `skip`: skip the Transforms (Default)
  - `only`: only run the Transforms (skip the Extract and Load steps)

### Examples

```bash
meltano select --exclude tap-carbon-intensity '*' 'longitude'
```

```bash
meltano select --exclude tap-carbon-intensity '*' 'latitude'
```

This will exclude all `longitude` and `latitude` attributes.

## `extract`

Extract data to a loader and optionally transform the data

### How to Use

```bash
meltano extract [name of extractor] --to [name of loader]`
```

## `init`

Used to create a new meltano project with a basic infrastructure in place in the current directory that the user is in.

### How to use

```bash
# Format
meltano init [project_name] [--no_usage_stats]
```

### Parameters

- **project_name** - This determines the folder name for the project

### Options

- **no_usage_stats** - This flag disables sending anonymous usage data when creating a new project.

## `install`

Installs all the dependencies of your project based on the **meltano.yml** file.

Use `--include-related` to automatically install transform, model, and dashboard plugins related to installed extractor plugins.

### How to Use

```bash
meltano install

meltano install --include-related
```

## `invoke`

- `meltano invoke <plugin_name> PLUGIN_ARGS...`: Invoke the plugin manually.

## `list`

Use `--list` to list the current selected tap attributes.

> Note: `--all` can be used to show all the tap attributes with their selected status.

## `permissions`

::: info
This is an optional tool for users who want to configure permissions if they're using Snowflake as the data warehouse and want to granularly set who has access to which data at the warehouse level.

Alpha-quality [Role Based Access Control (RBAC)](/developer-tools/role-based-access-control.html#role-based-access-control-rbac-alpha) is also available.
:::

Use this command to check and manage the permissions of a Snowflake account.

```bash
meltano permissions grant <spec_file> --db snowflake [--dry] [--diff]
```

Given the parameters to connect to a Snowflake account and a YAML file (a "spec") representing the desired database configuration, this command makes sure that the configuration of that database matches the spec. If there are differences, it will return the sql grant and revoke commands required to make it match the spec. If there are additional permissions set in the database this command will create the necessary revoke commands with the exception of:

* Object Ownership
* Warehouse Privileges

We currently support only Snowflake, as [pgbedrock](https://github.com/Squarespace/pgbedrock) can be used for managing the permissions in a Postgres database.

#### spec_file

The YAML specification file is used to define in a declarative way the databases, roles, users and warehouses in a Snowflake account, together with the permissions for databases, schemas and tables for the same account.

Its syntax is inspired by [pgbedrock](https://github.com/Squarespace/pgbedrock), with additional options for Snowflake.

All permissions are abbreviated as `read` or `write` permissions, with Meltano generating the proper grants for each type of object. This includes shared databases which have simpler and more limited permissions than non-shared databases.

Tables and views are listed under `tables` and handled properly behind the scenes.

If `*` is provided as the parameter for tables the grant statement will use the `ALL <object_type>s in SCHEMA` syntax. It will also grant to future tables and views. See Snowflake documenation for [`ON FUTURE`](https://docs.snowflake.net/manuals/sql-reference/sql/grant-privilege.html#optional-parameters)

If a schema name includes an asterisk, such as `snowplow_*`, then all schemas that match this pattern will be included in grant statement. This can be coupled with the asterisk for table grants to grant permissions on all tables in all schemas that match the given pattern. This is useful for date-partitioned schemas.

All entities must be explicitly referenced. For example, if a permission is granted to a schema or table then the database must be explicitly referenced for permissioning as well.

A specification file has the following structure:

```bash
# Databases
databases:
    - db_name:
        shared: boolean
    - db_name:
        shared: boolean
    ... ... ...

# Roles
roles:
    - role_name:
        warehouses:
            - warehouse_name
            - warehouse_name
            ...

        member_of:
            - role_name
            - role_name
            ...

        privileges:
            databases:
                read:
                    - database_name
                    - database_name
                    ...
                write:
                    - database_name
                    - database_name
                    ...
            schemas:
                read:
                    - database_name.*
                    - database_name.schema_name
                    - database_name.schema_partial_*
                    ...
                write:
                    - database_name.*
                    - database_name.schema_name
                    - database_name.schema_partial_*
                    ...
            tables:
                read:
                    - database_name.*.*
                    - database_name.schema_name.*
                    - database_name.schema_partial_*.*
                    - database_name.schema_name.table_name
                    ...
                write:
                    - database_name.*.*
                    - database_name.schema_name.*
                    - database_name.schema_partial_*.*
                    - database_name.schema_name.table_name
                    ...

        owns:
            databases:
                - database_name
                ...
            schemas:
                - database_name.*
                - database_name.schema_name
                - database_name.schema_partial_*
                ...
            tables:
                - database_name.*.*
                - database_name.schema_name.*
                - database_name.schema_partial_*.*
                - database_name.schema_name.table_name
                ...

    - role_name:
    ... ... ...

# Users
users:
    - user_name:
        can_login: boolean
        member_of:
            - role_name
            ...
    - user_name:
    ... ... ...

# Warehouses
warehouses:
    - warehouse_name:
        size: x-small
    ... ... ...
```

For a working example, you can check [the Snowflake specification file](https://gitlab.com/meltano/meltano/blob/master/tests/meltano/core/permissions/specs/snowflake_spec.yml) that we are using for testing `meltano permissions`.

#### --db

The database to be used, either `postgres` or `snowflake`. Postgres is still experimental and may be fully supported in the future.

#### --diff

When this flag is set, a full diff with both new and already granted commands is returned. Otherwise, only required commands for matching the definitions on the spec are returned.

#### --dry

When this flag is set, the permission queries generated are not actually sent to the server and run; They are just returned to the user for examining them and running them manually.

When this flag is not set, the commands will be executed on Snowflake and their status will be returned and shown on the command line.


#### Connection Parameters

The following environmental variables must be available to connect to Snowflake:

```bash
$PERMISSION_BOT_USER
$PERMISSION_BOT_PASSWORD
$PERMISSION_BOT_ACCOUNT
$PERMISSION_BOT_DATABASE
$PERMISSION_BOT_ROLE
$PERMISSION_BOT_WAREHOUSE
```

## `schedule`

::: tip
An `orchestrator` plugin is required to use `meltano schedule`: refer to the [Orchestration](/developer-tools/orchestration.html) documentation to get started with Meltano orchestration.
:::

Meltano provides a `schedule` method to run specified ELT pipelines at regular intervals. Schedules are defined inside the `meltano.yml` project as such:

- `meltano schedule <schedule_name> <extractor> <loader> <interval> [--transform]`: Schedule an ELT pipeline to run using an orchestrator.
  - `meltano schedule list`: List the project's schedules.

```yaml
schedules:
  - name: test
    interval: '@daily'
    extractor: tap-mock
    loader: target-mock
    transform: skip
    env: {}
```

## `select`

Use the `select` command to add select patterns to a specific extractor in your Meltano project.

- `meltano select [--list] [--all] <tap_name> [ENTITIES_PATTERN] [ATTRIBUTE_PATTERN]`: Manage the selected entities/attributes for a specific tap.

::: warning
Not all taps support this feature. In addition, taps needs to support the `--discover` switch. You can use `meltano invoke tap-... --discover` to see if the tap supports it.
:::

### How to use

Meltano select patterns are inspired by the [glob](<https://en.wikipedia.org/wiki/Glob_(programming)>) syntax you might find in your operating system.

- `*`: matches any sequence of characters
- `?`: matches one character
- `[abc]`: matches either `a`, `b`, or `c`
- `[!abc]`: matches any character **but** `a`, `b`, or `c`

### Examples

```bash
$ meltano select tap-carbon-intensity '*' 'name*'
```

This will select all attributes starting with `name`.

```bash
$ meltano select tap-carbon-intensity 'region'
```

This will select all attributes of the `region` entity.

::: tip
Most shells parse glob syntax: you must escape the special characters in the select pattern by quoting the pattern.
:::

### Exclude Parameter

Use `--exclude` to exclude all attributes that match the filter.

::: info
Exclusion has precedence over inclusion. If an attribute is excluded, there is no way to include it back without removing the exclusion pattern first.
:::

## `ui`

- `meltano ui`: Start the Meltano UI.

### `start` (default)

Start the Meltano UI.

### `setup`

::: tip
This command is only relevant for production-grade setup.
:::

Generate secure secrets in the `ui.cfg` so that the application is secure.

::: warning
Regenerating secrets will cause the following:

  - All passwords will be invalid
  - All sessions will be expired
  
Use with caution!
:::

#### --bits

Specify the size of the secrets, default to 256.

## `user`

::: tip
This command is only relevant when Meltano is run with authentication enabled.
:::

### `add` 

Create a Meltano user account, active and ready to be used.

#### --overwrite, -f

Update the user instead of creating a new one.

#### --role, -G

Add the user to the role. Meltano ships with two built-in roles: `admin` and `regular`.

#### How to use

```bash
meltano user add admin securepassword --role admin
```

## `upgrade`

Upgrade Meltano to the latest version.

This function will following process to upgrade Meltano:

- Run `pip3 install --upgrade meltano`
- Run the database migrations
- Send a [SIGHUP](http://docs.gunicorn.org/en/stable/signals.html#reload-the-configuration) to the process running under the `.meltano/run/gunicorn.pid`, thus restarting the workers

## `version`

It is used to check which version of Meltano currently installed.

### How to use

```bash
meltano --version
```