#!/bin/bash

mkdir syscalls2_out$1
java -jar negsel2.jar -self syscalls/snd-unm/Preprocessed/snd-unm.train.p -n 7 -r $1 -c 1 < syscalls/snd-unm/Preprocessed/snd-unm.1.test.p > syscalls2_out$1/snd-unm.1.test.out

java -jar negsel2.jar -self syscalls/snd-unm/Preprocessed/snd-unm.train.p -n 7 -r $1 -c 1 < syscalls/snd-unm/Preprocessed/snd-unm.2.test.p > syscalls2_out$1/snd-unm.2.test.out

java -jar negsel2.jar -self syscalls/snd-unm/Preprocessed/snd-unm.train.p -n 7 -r $1 -c 1 < syscalls/snd-unm/Preprocessed/snd-unm.3.test.p > syscalls2_out$1/snd-unm.3.test.out
