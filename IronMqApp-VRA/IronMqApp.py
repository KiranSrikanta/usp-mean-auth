__author__ = 'administrator'

from iron_mq import *
from time import sleep
from builtins import print
import json
from vRealizeAutomationRestClient import *

# Infinite loop. Is there a better scheduling mechanism?
while True:
    try:
        # Get the IronMQ queues. HARD CODING!
        ironMq = IronMQ(host="mq-aws-us-east-1.iron.io",
                        project_id="55b5ba3a258a0c0006000024",
                        token="dyM7fJMKZtjx-Qd5pkUfOb-Boak",
                        protocol="https", port=443,
                        api_version=1,
                        config_file=None)
        vraQueue = ironMq.queue("vra-queue")
        uspQueue = ironMq.queue("usp-queue")

        msg_all = vraQueue.get()

        if len(msg_all['messages']) > 0:
            for msg in msg_all['messages']:
                # deserialize json
                request = json.loads(msg['body'])

                if request['RequestId']:
                    # create request api call
                    request = get_request_by_id(request['RequestId'], None)

                else:
                    # Get vRA request status
                    request = create_request(request)

                # serialize json and post the message on the usp queue
                uspQueue.post(json.dumps(request))

                # delete the message
                vraQueue.delete(msg['id'])
        else:
            print("No messages are on queue")

    except Exception as e:
        print(e)

    sleep(60)
