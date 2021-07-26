# AirflowDevEnv
This repository details how to setup a development environment for AirFlow and then create some example web scraping DAGs.  This was as a direct result of seeing a job advert with these specific requirements.

This setup is a fully Docker container based approach that will show how to install AitFlow, install additional Python libraries, setup Postgres database access to store screen scraped information. Most of the information can be found on the Internet but I will undertake some additional configuration.

1. Install Docker and Docker-compose. https://docs.docker.com/

2. Install Docker setup of AirFlow. Download docker setup file from airflow.apache.org/docs/apache-airflow/2.1.2/docker-compose.yaml
Create a new Airflow directory somewhere convenient for you on your machine
Easiest way to do this is by using curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.2/docker-compose.yaml'

3. Using an editor of your choice open the docker-compose.yaml file downloaded and make the following changes:

**change** 
      AIRFLOW__CORE__LOAD_EXAMPLES: 'true' to AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
      **under** 
        services:
          postgres:
            image: postgres:13 
      **add**
            ports:
              - 5432:5432
    
The ports addition is because we are going to use the Postgres database that is deployed with the setup as our data store for the information we scrape.
Save and close the docker-compose file

4. Set up a new environment variable called _PIP_ADDITIONAL_REQUIREMENTS 
Mac Example
          export _PIP_ADDITIONAL_REQUIREMENTS="lxml"
          
5. Using a terminal window go to the directory that houses the docker-compose.yaml file

6. Type docker-compose up
This should start up the AirFlow environment

7. In a browser type, http://localhost:8080/health
You should see the following output
        {
            "metadatabase": {
                "status": "healthy"
            },
            "scheduler": {
                "status": "healthy",
                "latest_scheduler_heartbeat": "2021-07-26T14:11:43.156859+00:00"
            }
        }
        
 8. Type http://localhost:8080/ in browser and log into Airflow, Username/password is airflow/airflow
 9. Setting up a Postgres database Connector. This is used within our DAGs to connect to our database. Go to the Admin menu and select submenu Connections.
Fill in details as below
![image](https://user-images.githubusercontent.com/4700433/127004494-abbfc496-ba02-4506-a905-1eefa3f050f0.png)

10. Lets setup our database and table to hold our data. Using a Postgres database client such as pgAdmin4 or DBeaver connect to the database. The details you will need are Host:localhost Port:5432 Database:airflow Username:airflow Password:airflow
Create database called Data (you should be able to right click on the Airflow database in your Postgres client and select Create Database. Specify Airfloow as the Owner
11. Run the following SQL

        CREATE SEQUENCE public.test_id_seq
            INCREMENT 1
            START 1
            MINVALUE 1
            MAXVALUE 2147483647
            CACHE 1;
            
        ALTER SEQUENCE public.test_id_seq
            OWNER TO airflow;
            
        CREATE TABLE IF NOT EXISTS public.test
        (
            id integer NOT NULL DEFAULT nextval('test_id_seq'::regclass),
            title character varying COLLATE pg_catalog."default",
            url character varying COLLATE pg_catalog."default",
            created_at timestamp with time zone NOT NULL DEFAULT now()
        )

        TABLESPACE pg_default;

        ALTER TABLE public.test
            OWNER to airflow;


We should now have an environment that we can release our DAGs into and run where the output from these will be stored in a Postgres database.

          
