---
sidebar: auto
---

# Comma Separated Values (CSV)

`tap-csv` is a CSV reader that is optimized for tasks where the file structure is highly predictable.

## Info

- **Data Source**: Traditionally-delimited CSV files (commas separated columns, newlines indicate new rows, double quoted values) as defined by the defaults of the python csv library.
- **Repository**: [https://gitlab.com/meltano/tap-csv](https://gitlab.com/meltano/tap-csv)

## Install

1. Navigate to your Meltano project in the terminal
2. Run the following command:

```bash
meltano add extractor tap-csv
```

If you are successful, you should see `Added and installed extractors 'tap-csv'` in your terminal.

## Configuration

**.env**

```bash
export TAP_CSV_FILES_DEFINITION="files_def.json"
```

Where `files_def.json` is a json file with all the CSV files to be loaded:

**files_def.json**

```json
[
  { "entity": "leads", "file": "/path/to/leads.csv", "keys": ["Id"] },
  {
    "entity": "opportunities",
    "file": "/path/to/opportunities.csv",
    "keys": ["Id"]
  }
]
```

Description of available options:

- **entity**: The entity name to be passed to singer (i.e. the table name).
- **file**: Local path to the file to be ingested. Note that this may be a directory, in which case all files in that directory and any of its subdirectories will be recursively processed.
- **keys**: The names of the columns that constitute the unique keys for that entity.