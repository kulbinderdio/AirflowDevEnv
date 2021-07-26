
from lxml import html
import requests
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG('reuters_database_insert',
    start_date=days_ago(2),
    schedule_interval=None,
    catchup=False,
    template_searchpath="."
    ) as dag:
    

    def get_headlines():
        reuters_web = 'https://www.reuters.com/news/archive/businessNews'
        response = requests.get(reuters_web)

        # //h3[@class="fc-item__title"]/a@href

        tree = html.fromstring(response.content)
        stories = tree.xpath('//article[@class="story "]/div/a')

        with open("reuters_inserts.sql","w") as f:

            for story in stories:
                if len(story.xpath('@href')) > 0 and len(story.xpath('h3/text()'))>0:
                    url = story.xpath('@href')[0]
                    title = story.xpath('h3/text()')[0].strip().replace("'","")
                    print("***" + title)
                    if url:
                        sql = f"INSERT INTO test (title, url) VALUES ('{title}', '{reuters_web+url}');\n"
                        print(sql)
                        f.write(sql)





    download_reuters_stories = PythonOperator(
    	task_id="save_reuters_story_sql",
    	python_callable = get_headlines,
    	dag=dag,
    )

    write_to_database =  PostgresOperator(
        task_id="write_to_database",
        postgres_conn_id="postgres_sql",
        sql="reuters_inserts.sql",
        dag=dag,
    )
    download_reuters_stories >> write_to_database
