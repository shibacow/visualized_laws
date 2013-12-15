#!/bin/bash
rm -rf dump
mongodump -d laws
tar cjvf dump.tar.bz2 dump
rm -rf dump
