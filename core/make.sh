#!/bin/bash
cd judged
make
chmod +x judged
cp judged /usr/bin
cd ../judge_client
make
chmod +x judge_client
cp judge_client /usr/bin

