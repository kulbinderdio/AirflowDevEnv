
from lxml import html
import requests
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG('guardian_database_insert',
    start_date=days_ago(2),
    schedule_interval=None,
    catchup=False,
    template_searchpath="."
    ) as dag:
    

    def get_headlines():
        response = requests.get('https://www.theguardian.com/uk/business')

        # //h3[@class="fc-item__title"]/a@href

        tree = html.fromstring(response.content)
        stories = tree.xpath('//h3[@class="fc-item__title"]/a')

        with open("inserts.sql","w") as f:

            for story in stories:
                url = story.xpath('@href')
                title = story.xpath('span/span/text()')
                if title:
                    sql = f"INSERT INTO test (title, url) VALUES ('{title[0]}', '{url[0]}');\n"
                    print(sql)
                    f.write(sql)





    download_guardian_stories = PythonOperator(
    	task_id="save_guardian_story_sql",
    	python_callable = get_headlines,
    	dag=dag,
    )

    write_to_database =  PostgresOperator(
        task_id="write_to_database",
        postgres_conn_id="postgres_sql",
        sql="inserts.sql",
        dag=dag,
    )
    download_guardian_stories >> write_to_database
