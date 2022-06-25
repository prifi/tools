#!/usr/bin/env python
# coding:utf-8
# @返回当前mq列表

import json, requests, optparse

class RabbitMQMoniter(object):
    """
    RabbitMQ Management API
    """
    def __init__(self, host='', port=15672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def call_api(self, path):
        headers = {'content-type': 'application/json'}
        url = '{0}://{1}:{2}/api/{3}'.format('http', self.host, self.port, path)
        res = requests.get(url, headers=headers, auth=(self.username, self.password))
        return res.json()

    def list_queues(self):
        """
        curl -i -u guest:guest http://localhost:15672/api/queues
        return: list
        """
        queues = []
        queues_dict = {"data": None}
        for queue in self.call_api('queues'):
            #tmp_dict = {}
            #tmp_dict["{#QUEUE_NAME}"] =  str("".join(queue['name'])),
            #tmp_dict["{#QUEUE_COUNT}"] = queue['messages']
            #queues.append(tmp_dict)

            element = {
                '{#QUEUE_NAME}': str("".join(queue['name'])),
                #'{#QUEUE_COUNT}': queue['messages']
            }
            queues.append(element)

        queues_dict['data'] = queues
        return queues_dict

        #queues_dict["data"] = queues
        #return queues_dict

def main():
    parser = optparse.OptionParser()
    parser.add_option('--username', help='RabbitMQ API username', default='guest')
    parser.add_option('--password', help='RabbitMQ API password', default='guest')
    parser.add_option('--host', help='RabbitMQ API host', default='127.0.0.1')
    parser.add_option('--port', help='RabbitMQ API port', type='int', default=15672)
    (options, args) = parser.parse_args()
    api = RabbitMQMoniter(username=options.username, password=options.password, host=options.host, port=options.port)
    #api.list_queues()
    jsonStr = json.dumps(api.list_queues(), sort_keys=True, indent=4)
    print(jsonStr)

if __name__ == '__main__':
    main()