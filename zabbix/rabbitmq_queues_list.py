#!/usr/bin/env python
# coding:utf-8
# @返回某一个队列的堆积值，参数：[mq_name]

import sys, json, requests, optparse

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
        queues = {}
        for queue in self.call_api('queues'):
            queues[str("".join(queue['name']))] =  queue['messages']

        return queues

def main():
    parser = optparse.OptionParser()
    parser.add_option('--username', help='RabbitMQ API username', default='guest')
    parser.add_option('--password', help='RabbitMQ API password', default='guest')
    parser.add_option('--host', help='RabbitMQ API host', default='127.0.0.1')
    parser.add_option('--port', help='RabbitMQ API port', type='int', default=15672)
    (options, args) = parser.parse_args()
    api = RabbitMQMoniter(username=options.username, password=options.password, host=options.host, port=options.port)
    result = api.list_queues()
    print(result[sys.argv[1]])

if __name__ == '__main__':
    main()