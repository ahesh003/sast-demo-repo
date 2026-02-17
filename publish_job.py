# import json
# import pika
# import time
# import uuid


# # Wait for 5 seconds to give RabbitMQ time to start up
# time.sleep(5)

# def wait_for_rabbitmq(host="rabbitmq", retries=10, delay=3):
#     for attempt in range(retries):
#         try:
#             return pika.BlockingConnection(
#                 pika.ConnectionParameters(host=host)
#             )
#         except pika.exceptions.AMQPConnectionError:
#             print(f"[MCP] RabbitMQ not ready, retrying ({attempt + 1}/{retries})...")
#             time.sleep(delay)
#     raise RuntimeError("RabbitMQ not reachable after retries")

# # Define the job payload that will be sent to RabbitMQ
# # This dictionary represents a SAST (Static Application Security Testing) scan job
# job = {
#     "job_id": str(uuid.uuid4()),
#     "scan_type": "sast",
#     "repo": {
#         "type": "git",
#         "url": "https://github.com/ahesh003/sast-demo-repo.git",
#         "branch": "main"
#     },

#     # Path inside the worker container where SAST rules are stored
#     "rules_path": "/rules/semgrep-rules"
# }


# # Create a blocking (synchronous) connection to RabbitMQ
# # "rabbitmq" is the Docker service name
# # connection = pika.BlockingConnection(
# #     pika.ConnectionParameters(host="rabbitmq")
# # )

# connection = wait_for_rabbitmq()
# # Open a channel on the connection
# channel = connection.channel()

# # Declaring a queue named "sast_jobs"
# # durable=True ensures the queue survives RabbitMQ restarts
# channel.queue_declare(
#     queue="sast_jobs",
#     durable=True
# )

# # Publish the job message to RabbitMQ
# channel.basic_publish(
#     exchange="",              # Default exchange (direct routing)
#     routing_key="sast_jobs",  # Name of the queue to send the message to
#     body=json.dumps(job),     # Convert the job dictionary to a JSON string
#     properties=pika.BasicProperties(
#         delivery_mode=2       # Make the message persistent (saved to disk)
#     ),
# )

# # Log the published job ID for visibility/debugging
# print(f"[MCP] Published job {job['job_id']}")

# # Close the connection cleanly
# connection.close()

# -----------------------------------------------------------------------------------------------
import pika
import json
import sys
import os

job_file = sys.argv[1]

with open(job_file) as f:
    job = json.load(f)

rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = int(os.environ.get("RABBITMQ_PORT", "5672"))
rabbitmq_user = os.environ.get("RABBITMQ_USER")
rabbitmq_pass = os.environ.get("RABBITMQ_PASS")

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        credentials=credentials
    )
)

channel = connection.channel()
channel.queue_declare(queue="sast_jobs", durable=True)

channel.basic_publish(
    exchange="",
    routing_key="sast_jobs",
    body=json.dumps(job),
    properties=pika.BasicProperties(delivery_mode=2)
)

print(f"[Jenkins] Published job {job['job_id']} to {rabbitmq_host}:{rabbitmq_port}")

connection.close()




