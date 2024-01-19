#!/bin/bash

poetry export --with local --format requirements.txt --output requirements/local.txt --all-extras
