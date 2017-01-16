#!/usr/bin/bash
cat matrix.def-original-* | gunzip -c > matrix.def
gunzip -c lex.csv-original.gz > lex.csv.original
