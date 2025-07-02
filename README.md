# parulidae

## Overview

This repo hosts code and data for running the [warbler dashboard](https://warbler.streamlit.app), hosted by streamlit.
The dashboard summarizes audio recordings of warblers in the United States 
that have been contributed to [Xeno-canto](https://xeno-canto.org), a global repository of nature sound 
recordings shared under Creative Commons licenses. It demonstrates how web service 
usage can be analyzed over time, across contributors, and by content type.

## Repo contents

  - [Welcome.py](Welcome.py): The start page for the dashboard app.
  - [pages](pages): A directory for all other dashboard pages.
  - [app_utils](app_utils): Modules required for generating the dashboard pages.
  - [dev_utils](dev_utils): Modules used in preparing the data sets.
  - [data](data): Raw and cleaned data generated with [dev_utils/data.py](dev_utils/data.py).
  - [pyproject.toml](pyproject.toml): Poetry file for managing the virtual environment.
  - [requirements.txt](requirements.txt): Requirements file required for streamlit hosting of dashboard.

## Using the repo

First, set up the virtual environment using poetry:

```bash
pip install poetry
poetry install
poetry shell
```

Now the dashboard app may be run locally with streamlit:

```bash
streamlit run Welcome.py
```

Optionally, the data may be updated by following a few steps:

  1. Register for a [Xeno-canto](https://xeno-canto.org/) account and find your API key under
     your [account page](https://xeno-canto.org/explore/api).
  2. Create a file named .env and store the API key as `XENOCANTO_API_KEY=xxxx`.
  3. Update the data from Xeno-canto with `python dev_utils/data.py`.


## About

This project relies on data retrieved from [xeno-canto.org](https://xeno-canto.org/)
and photographs from [inaturalist.org](https://www.inaturalist.org/),
all of which are made available under Creative Commons licenses. Individual creators
are credited within the dashboard wherever their works are referenced. 
The project itself is licensed under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0).
