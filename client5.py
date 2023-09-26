import json
import time
from google.cloud import pubsub_v1
from google.auth import jwt
from secret import project_id,topic_name


service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials = jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience
)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(project_id, topic_name)

# Creo il topic, canale tematico
try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)

# Creo messaggio
with open('5.txt') as f:
    for r in f:
        r = r.strip()
        print("sending: ", r)
        r = publisher.publish(topic_path, str(r).encode('utf-8'))
        time.sleep(1)
