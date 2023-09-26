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
