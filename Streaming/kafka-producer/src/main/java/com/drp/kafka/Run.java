package com.drp.kafka;

import java.io.IOException;

/**
 * Code to run the producer.
 */
public class Run {
    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            throw new IllegalArgumentException("Must have either 'producer' as argument");
        }
        switch (args[0]) {
            case "producer":
                Producer.main(args);
                break;
            default:
                throw new IllegalArgumentException("Don't know how to do " + args[0]);
        }
    }
}
