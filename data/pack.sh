#!/bin/bash
for i in *.csv ; do 
  gzip --best $i ; 
done
