package com.drp.kafka;

import com.google.common.io.Resources;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
/**
 * This producer will send a bunch of messages to topic "fast-messages". Every so often,
 * it will send a message to "slow-messages". This shows how messages can be sent to
 * multiple topics. On the receiving end, we will see both kinds of messages but will
 * also see how the two topics aren't really synchronized.
 */


public class Producer {

    public static void main(String[] args) throws IOException {
        // set up the producer
        KafkaProducer<String, String> producer;
        try (InputStream props = Resources.getResource("producer.props").openStream()) {
            Properties properties = new Properties();
            properties.load(props);
            producer = new KafkaProducer<>(properties);
        }
        try {
            GsonBuilder builder = new GsonBuilder();
            Gson gson = builder.create();
            /*
            Segment S = new Segment();
            for (int i = 0; i < 100; i++) {

                S.startlat = Math.random() * 90 + 1;
                S.startlong = Math.random() * 90 + 1;
                S.cost = Math.random() * 90 + 1;
                S.endlat = Math.random() * 90 + 1;
                S.endlong = Math.random() * 90 + 1;*/
                producer.send(new ProducerRecord<String, String>("segments", gson.toJson(S)));
                producer.flush();
                System.out.println("Sent msg number " + i);
            }
        } catch (Throwable throwable) {
            System.out.printf("%s", throwable.getStackTrace());
        } finally {
            producer.close();
        }

    }
}
