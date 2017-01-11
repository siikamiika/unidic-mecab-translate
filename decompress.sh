#!/usr/bin/bash
cat matrix.def-original-* | gunzip -c > matrix-original.def
gunzip -c lex.csv-original.gz > lex-original.csv
