

# Distributed Route Planning Project
### Readme for Spark + Kafka Streaming 
 
 This directory provides a tar of the kafka version we're using, and the python code for the direct streaming spark application we're developing. A built Spark installation is assumed; we are using version 1.6.0. To work with the python code, copy it into the **examples/src/main/python/streaming/** directory of your spark installation and execute the following from the Spark directory to run: 
```
 bin/spark-submit --jars \
      external/kafka-assembly/target/scala-*/spark-streaming-kafka-assembly-*.jar \
      examples/src/main/python/streaming/distributed_route_streaming.py localhost:9092 test
```
> Note that to run this on your local machine, you need to setup Kafka and create a producer first, see: http://kafka.apache.org/documentation.html#quickstart

### Troubleshooting

An issue that may arise when attempting to run the python code where the program cannot find the .jar files, if this happens try removing **scala-*** from the **external/kafka-assembly/target/scala-*/spark-streaming-kafka-assembly-*.jar** filepath.
