#!/bin/bash

mkdir out$1
java -jar negsel2.jar -self english.train -n 10 -r $1 -c 1 < english.test > out$1/english.test.out
java -jar negsel2.jar -self english.train -n 10 -r $1 -c 1 < tagalog.test > out$1/tagalog.test.out
java -jar negsel2.jar -self english.train -n 10 -r $1 -c 1 < lang/plautdietsch.txt > out$1/plautdietsch.test.out
java -jar negsel2.jar -self english.train -n 10 -r $1 -c 1 < lang/middle-english.txt > out$1/middle-english.test.out
java -jar negsel2.jar -self english.train -n 10 -r $1 -c 1 < lang/hiligaynon.txt > out$1/hiligaynon.test.out
java -jar negsel2.jar -self english.train -n 10 -r $1 -c 1 < lang/xhosa.txt > out$1/xhosa.test.out

