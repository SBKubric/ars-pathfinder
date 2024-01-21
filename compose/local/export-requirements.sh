#!/bin/bash

poetry export --with local --with monitoring --format requirements.txt --output requirements/local.txt --all-extras
