#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
 Counts words in UTF8 encoded, '\n' delimited text directly received from Kafka in every 2 seconds.
 Usage: direct_kafka_wordcount.py <broker_list> <topic>

 To run this on your local machine, you need to setup Kafka and create a producer first, see
 http://kafka.apache.org/documentation.html#quickstart

 and then run the example
    `$ bin/spark-submit --jars \
      external/kafka-assembly/target/scala-*/spark-streaming-kafka-assembly-*.jar \
      examples/src/main/python/streaming/distributed_route_streaming.py \
      localhost:9092 test`
"""

import sys
import json

from mysql.connector import (connection)
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    if len(sys.argv) != 3:
        #print("Usage: direct_kafka_wordcount.py <broker_list> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonStreamingDistributedRoute")
    ssc = StreamingContext(sc, 2)
    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})

    # Open a database connection and save into the segments table based on whats in the kafka message.
    def saveJsontoSQL(r):
        sqlConnection = connection.MySQLConnection(user='root', database='DRPdev', password='bananas', host='localhost')
        cursor=sqlConnection.cursor()
        add_segment = ("INSERT INTO segments "
               "(startlat, startlong, cost, endlat, endlong) "
               "VALUES (%(startlat)s, %(startlong)s, %(cost)s, %(endlat)s, %(endlong)s)")
        parsedJson = json.loads(r[1])
        lat1 = str(parsedJson["startlat"])
        long1 = str(parsedJson["startlong"])
        cost = str(parsedJson["cost"])
        lat2 = str(parsedJson["endlat"])
        long2 = str(parsedJson["endlong"])
        segment = {'startlat': lat1,
                   'startlong': long1,
                   'cost': cost,
                   'endlat': lat2,
                   'endlong': long2}
        cursor.execute(add_segment, segment)
        sqlConnection.commit()
        cursor.close()
        sqlConnection.close()


    parsed = kvs.map(saveJsontoSQL)
    parsed.pprint()
    
    ssc.start()
    ssc.awaitTermination()