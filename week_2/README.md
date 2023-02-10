## Data Engineering Zoomcamp 2023 Week 2

## Prefect
This repo contains Python code to accompany the videos that show how to use Prefect for Data Engineering. We will create ETL workflows to extract, transform, and load your data.

We will use Postgres and GCP's Google Cloud Storage and BigQuery.

Prefect helps you observe and orchestrate your dataflows.

## Setup

### Create virtual environment
In project folder use terminal
```commandline
python -m venv zoomcamp
```
Activate virtual environment
```commandline
zoomcamp\Scripts\activate
```

### Install packages
In a `zoomcamp` environment, install all package dependencies with

```
pip install -r requirements.txt
```

### Start the Prefect Orion server locally
Create another window and activate `zoomcamp` environment. Start the Orion API server locally with

```
prefect orion start
```

## Set up GCP
* Log in to GCP
* Create a Project
* Set up Cloud Storage
* Set up BigQuery
* Create a service account with the required policies to interact with both services

Described in week_1\1_terraform_gcp


## Register the block types that come with prefect-gcp
In Orion UI create block type "SQLAlchemyConnector".

```text
prefect block register -m prefect_gcp
```

## Create Prefect GCP blocks
Create a GCP Credentials block in the Orion UI:
* Block Name - as you want
* Service Account File - Paste service account information from JSON file (week_1\1_terraform_gcp\gcp_owerview.md)

Create a GCS Bucket block in UI:
* Block Name - as you want
* Bucket - Bucket name from GCS (Google Cloud/Cloud Storage/Buckets)
* Gcp Credentials - Dropdown list with GCP Credentials blocks

Alternatively, create these blocks using code by following the templates in the blocks folder.

## Create flow code
Write Python functions and add @flow and @task decorators.

Note file paths for store  `.parquet` file.

Add two files with parametrized flow (1 for web_to_gcs flow, 1 for gcs_to_bq flow).

## Create deployments
Create and apply deployments. 
### Deployment on the CLI
* Build. Will create `.yaml`-file with all parameters of deployment. You can add parameters (year, months, color) into `.yaml`-file
```commandline
prefect deployment build ./parametrized_gcs_to_bq.py:main_flow -n "Parametrized GCS to BQ flow"
```
* Apply. You can see deployment parameters into Orion UI. Press button "Quick run". And go to "Work Queues / default" section to run Agent
"
```commandline
prefect deployment apply main_flow-deployment.yaml
```
* Agent. Will run deployment task.
```commandline
prefect agent start --work-queue "default"
```
Make sure your agent set up to poll the work queue you created when you made your deployment (default if you didn't specify a work queue).

## Create GitHub block
Create GitHub block using Orion UI.
Or use Python code alternatively
```text
from prefect.filesystems import GitHub

github_block = GitHub(
    name = "zoom-github", 
    repository = "https://github.com/andreishvaidyuk/de_zoomcamp/tree/main/week_2"
)
github_block.save("zoom-github", overwrite=True)
```
Build deployment
* ```prefect deployment build ./parametrized_web_to_gcs.py:etl_parent_flow -n "github deployment" -sb github/zoom-github```
* ```prefect deployment apply etl_parent_flow-deployment.yaml```
* ```prefect agent start -q 'default'```

## Create Notification
Create Notification using Orion UI.
In the Prefect Orion UI create a Notification to send a Slack message when a flow run enters a Completed state. Here is the Webhook URL to use: https://hooks.slack.com/services/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

