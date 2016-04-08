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
 Recieves team 1 info stream in UTF8 encoded, '\n' delimited text directly received from Kafka in every 2 seconds.
 Usage: drpstream.py <broker_list> <topic>

 To run this on your local machine, you need to setup Kafka and create a producer first, see
 http://kafka.apache.org/documentation.html#quickstart

 and then run the example
    `$ bin/spark-submit --jars \
      external/kafka-assembly/target/scala-*/spark-streaming-kafka-assembly-*.jar \
      examples/src/main/python/streaming/drpstream.py \
      localhost:9092 test`
"""

import sys
import json

# The following are imported
import psycopg2
import psycopg2.extras
import Geohash
import pghstore

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    if len(sys.argv) != 3:
        #print("Usage: direct_kafka_wordcount.py <broker_list> <topic>", file=sys.stderr)
        exit(-1)

    # Create a streaming context for our application with a 5 second batch duration.
    sc = SparkContext(appName="PythonStreamingDistributedRoute")
    ssc = StreamingContext(sc, 5)
    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})


    # Open a database connection and save into the segments table based on whats in the kafka message.
    def costAlgo(r):
        parsedJson = json.loads(r[1])
        # This needs to change depending on the stream information. Then we handle that and calculate cost.
        fromHash = str(parsedJson["from"])
        geohash = Geohash.encode(fromHash.get("lat"),fromHash.get("lon"), 9)
        dest = str(parsedJson["to"])
        toHash = Geohash.encode(dest.get("lat"),dest.get("lon"), 8)

        keyHash = str(parsedJson["key"])
        tStamp = str(parsedJson["timestamp"])
        value = str(parsedJson["value"])

        # Try to connect and insert into our database
        try:
            conn = psycopg2.connect("dbname='DRP' user='postgres' password='bananas'")
        except:
            print "I am unable to connect to the database."

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            result = None

            while result == None:
                cur.execute("""SELECT * FROM geohashed_ways WHERE geohash LIKE  """ + "'" + geohash + "'%;")
                result = cur.fetchone()
                geohash = geohash[:-1]

        except:
            print "I can't SELECT."

        # Compute the cost using the updated data that was streamed and data already existing in our database.
        tagDict = pghstore.loads(result['tags'])
        isAccident = False
        if keyHash == 'TRAFFIC_INCIDENT':
            cost = value*10
            isAccident = True
        else:
            cost = value

        for k,v in tagDict:
            if k == 'lanes':

                if tagDict[k] == 2 and result['oneway'] == 'yes':
                    if isAccident:
                        cost=cost+(value*10)
                    else:
                        cost=cost+20
                elif tagDict[k] == 2 and result['oneway'] == 'no':
                    if isAccident:
                        cost=cost+(value*5)
                    else:
                        cost=cost+15
                elif tagDict[k] > 2 and result('oneway') == 'yes':
                    if isAccident:
                        cost=cost+(value*5)
                    else:
                        cost=cost+10
                elif tagDict[k] > 2 and result('oneway') == 'no':
                    if isAccident:
                        cost=cost+(value*2)
                    else:
                        cost=cost+5

            elif k == 'highway':
                if tagDict[k] == 'primary':
                    cost=cost-20
                elif tagDict[k] == 'secondary':
                    cost=cost-15
                elif tagDict[k] == 'trunk':
                    cost=cost-10
                elif tagDict[k] == 'trunk_link':
                    cost=cost-5

            elif k == 'maxspeed':
                if tagDict[k] >= 50:
                    cost = cost-tagDict[k]
                else:
                    cost = cost+tagDict[k]

        try:
            # Insert the updated cost for the way into our database.
            cur.execute("""INSERT INTO ways cost VALUES """ + cost + " where way.id=" + result['id'] + ';')
        except:
            print "I can't INSERT"
        cur.close()
        conn.close()


    parsed = kvs.map(costAlgo)
    parsed.pprint()

    ssc.start()
    ssc.awaitTermination()
