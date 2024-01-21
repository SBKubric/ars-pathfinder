#!/bin/bash

poetry export --with monitoring --format requirements.txt --output requirements/monitoring.txt --all-extras
