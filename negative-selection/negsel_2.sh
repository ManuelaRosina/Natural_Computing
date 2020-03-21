#!/bin/bash

mkdir syscalls_out$1
java -jar negsel2.jar -self syscalls/snd-cert/Preprocessed/snd-cert.train.p -n 7 -r $1 -c 1 < syscalls/snd-cert/Preprocessed/snd-cert.1.test.p > syscalls_out$1/snd-cert.1.test.out

java -jar negsel2.jar -self syscalls/snd-cert/Preprocessed/snd-cert.train.p -n 7 -r $1 -c 1 < syscalls/snd-cert/Preprocessed/snd-cert.2.test.p > syscalls_out$1/snd-cert.2.test.out

java -jar negsel2.jar -self syscalls/snd-cert/Preprocessed/snd-cert.train.p -n 7 -r $1 -c 1 < syscalls/snd-cert/Preprocessed/snd-cert.3.test.p > syscalls_out$1/snd-cert.3.test.out
