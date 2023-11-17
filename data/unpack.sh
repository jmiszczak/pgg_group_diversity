#!/bin/bash
for i in *.csv.gz ; do 
  gunzip $i ; 
done
