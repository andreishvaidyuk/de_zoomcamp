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


##Register the block types that come with prefect-gcp
In Orion UI create block type "SQLAlchemyConnector".

```text
prefect block register -m prefect_gcp
```

##Create Prefect GCP blocks
Create a GCP Credentials block in the Orion UI:
* Block Name - as you want
* Service Account File - Paste service account information from JSON file (week_1\1_terraform_gcp\gcp_owerview.md)

Create a GCS Bucket block in UI:
* Block Name - as you want
* Bucket - Bucket name from GCS (Google Cloud/Cloud Storage/Buckets)
* Gcp Credentials - Dropdown list with GCP Credentials blocks

Alternatively, create these blocks using code by following the templates in the blocks folder.

##Create flow code
Write Python functions and add @flow and @task decorators.

Note file paths for store  `.parquet` file.

##Create deployments
Create and apply your deployments.

##Run a deployment or create a schedule
Run a deployment ad hoc from the CLI or UI.

Or create a schedule from the UI or when you create your deployment.

##Start an agent
Make sure your agent set up to poll the work queue you created when you made your deployment (default if you didn't specify a work queue).

##Later: create a Docker Image and use a DockerContainer infrastructure block
Bake your flow code into a Docker image, create a DockerContainer, and your flow code in a Docker container.

##Optional: use Prefect Cloud for added capabilties
Signup and use for free at https://app.prefect.cloud