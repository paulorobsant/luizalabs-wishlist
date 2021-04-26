#!/bin/bash

while getopts u:a:f: flag
do
    case "${flag}" in
        n) name=${OPTARG};;
        m) message=${OPTARG};;
    esac
done

alembic \
    --name=$name \
    revision \
    --message=$message \
    --head=$name@head
    --autogenerate