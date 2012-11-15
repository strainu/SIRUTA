#!/bin/bash

cd doc
make installhtml
cd -
python setup.py sdist
