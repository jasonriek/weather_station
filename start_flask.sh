#!/bin/bash
export FLASK_APP=weather_app.py
export FLASK_ENV=production
flask run --host=0.0.0.0 --port=52007
