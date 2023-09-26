def save_data_2_bq(event, context):
    import base64
    from google.cloud import bigquery
    from json import loads
    from base64 import b64decode
    from datetime import datetime, timedelta

    print("""This Function was triggered by messageId {} published at {} to {}
    """.format(context.event_id, context.timestamp, context.resource["name"]))

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'Error'
    print(format(name))

    num, datetime, lon, lat = name.split(',')

    client = bigquery.Client()
    project_id = 'progetto-pcsc'
    dataset_id = 'dataset'
    table_id = 'tabella'
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'

    rows = [{'num': num, 'datetime': datetime, 'lat': lat, 'lon': lon}]
    errors = client.insert_rows_json(table_full_id, rows)  # Make an API request.
    if errors == []:
        return "New rows have been added."
    else:
        return "Encountered errors while inserting rows: {}".format(errors)

def last_locations(request):
    from flask import render_template
    from google.cloud import bigquery
    from google.oauth2 import service_account

    key_path = "credentials.json"

    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    query = """
        select num, datetime, lat, lon
        from `progetto-pcsc.dataset.tabella` t1
        where datetime = (select max(datetime) from `progetto-pcsc.dataset.tabella` t2 where t1.num = t2.num)
        group by num, datetime, lat, lon
    """
    query_job = client.query(query)  # Make an API request.

    geo = []
    for row in query_job:
        geo.append([row[0], row[2], row[3]])

    return render_template('index.html', geo=geo)
def trajectory(request):
    from flask import render_template
    from google.cloud import bigquery
    from google.oauth2 import service_account

    key_path = "credentials.json"

    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    query = """
         select num, datetime, lat, lon  
         from `progetto-pcsc.dataset.tabella` t1
         order by TIMESTAMP(datetime) 

     """
    query_job = client.query(query)  # Make an API request.

    num = []
    for row in query_job:
        num.append(row[0])

    num.sort()

    data = []
    for row in query_job:
        data.append([row[0], row[2], row[3]])

    return render_template('form.html', num=num, data=data)