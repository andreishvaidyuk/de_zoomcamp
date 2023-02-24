<<<<<<< HEAD
Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [dbt community](http://community.getbdt.com/) to learn from other analytics engineers
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
=======
## Load files directly to GCS. 
Downloads csv files from https://nyc-tlc.s3.amazonaws.com/trip+data/ and uploads them to your Cloud Storage Account as parquet files.

- Install pre-reqs (more info in web_to_gcs.py script)
- Run: python web_to_gcs.py

## Setting up dbt for using BigQuery 
You will need to create a dbt cloud account using [this link](https://www.getdbt.com/signup/) and connect to your warehouse [following these instructions](https://docs.getdbt.com/docs/dbt-cloud/cloud-configuring-dbt-cloud/cloud-setting-up-bigquery-oauth). 

### Create a dbt cloud project
- Once you have logged in into dbt cloud you will be prompt to create a new project
- Name your project
- Choose Bigquery as your data warehouse
- Upload the key you downloaded from BQ on the `create from file` option. This will fill out most fields related to the production credentials. Scroll down to the end of the page and set up your development credentials.
- Click on `Test` and after that you can continue with the setup

### Add GitHub repository
- Select git clone and paste the SSH key from your repo.
- You will get a deploy key, head to your GH repo and go to the settings tab. Under security you'll find the menu deploy keys. Click on add key and paste the deploy key provided by dbt cloud. Make sure to tikce on "write access"

### Review your project settings

## Starting a dbt project
### Using BigQuery + dbt cloud
>>>>>>> 77790a573236aece4389dac8c29986070c8bb436
