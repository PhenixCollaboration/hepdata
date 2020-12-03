#!/bin/bash

echo Making a tar file with the name $1.tar
tar -cvf $1.tar *.yaml *.png
