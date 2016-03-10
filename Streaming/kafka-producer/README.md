# Sample Programs for Kafka 0.9 API

Tutorial here:

https://www.mapr.com/blog/getting-started-sample-programs-apache-kafka-09

To start up the kafka stuff:

1)Start zookeeper:

bin/zookeeper-server-start.sh config/zookeeper.properties

2)Start kafka server:

bin/kafka-server-start.sh config/server.properties

3)List the topics just to check:

bin/kafka-topics.sh --list --zookeeper localhost:2181

4)Start the spark stream on a topic

bin/spark-submit --jars external/kafka-assembly/target/scala-*/spark-streaming-kafka-assembly-*.jar examples/src/main/python/streaming/distributed_route_streaming.py localhost:9092 test

5)Go to the kafka-producer folder and run the java code 

To list all messages in a topic called 'test':

target/kafka-producer producer

bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning
