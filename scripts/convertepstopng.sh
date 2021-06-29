#!/bin/bash
for f in `ls *.eps`; do
     convert -density 200 $f -flatten ${f%.*}.png;
done
