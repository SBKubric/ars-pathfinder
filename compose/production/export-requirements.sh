#!/bin/bash

poetry export --with production --format requirements.txt --output requirements/production.txt --all-extras
