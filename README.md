# errbot-maya-plugin

This plugin is an interface for [maya](https://droposhado.org/projects/maya),
adding and removing in MongoDB using mongoengine, to later generate the storage
dump and [maya](https://droposhado.org/projects/maya) is a health data collection,
storage and processing project, where the focus is on the collected data.

- <= 1.1.0 use MongoDB as storage;
- >= 1.2.0 use PostgreSQL as storage;

## Requirements

- **sqlalchemy[postgresql_psycopg2binary]** is need by SQLAlchemy to connect on
  PostgreSQL.

## Usage

**Add** liquid:

```
<prefix>maya liquid add <type> <quantity>
<prefix>maya liquid add coffee 80
<prefix>maya liquid add water 80

<prefix>maya liquid add <type> <quantity> <date>
<prefix>maya liquid add coffee 80 2022-05-25T01:01:01Z
<prefix>maya liquid add water 80 2022-05-25T01:01:01Z
```

Where `date` is `YYYY-MM-DDTHH:MM:SSZ`.

**List** liquid:

```
<prefix>maya liquid list <type>
<prefix>maya liquid list coffee
<prefix>maya liquid list water

<prefix>maya liquid list <type> <date>
<prefix>maya liquid list coffee 2022-05-25
<prefix>maya liquid list water 2022-05-25
```

Where `date` is `YYYY-MM-DD`.

**Remove** liquid:

```
<prefix>maya liquid remove <type> <uuid>
<prefix>maya liquid remove coffee 00000000-0000-0000-0000-000000000000
<prefix>maya liquid remove water 00000000-0000-0000-0000-000000000000
```

Where `00000000-0000-0000-0000-000000000000` must be a valid v4 UUID.

## License

See [LICENSE](LICENSE).
