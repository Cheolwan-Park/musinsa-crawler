#!/bin/bash

dockerize -wait http://chrome:4444 -timeout 20s

echo "Run Crawler!"
python -m musinsa_crawler