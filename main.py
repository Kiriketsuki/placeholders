from operator import mul

import flask
from website import createApp, initialize_db
# import sentry_sdk
from flask import Flask, config
# from sentry_sdk.integrations.flask import FlaskIntegration
import multiprocessing

# sentry_sdk.init(
#     dsn="https://b8534193d8bb4c78b00e134d989d915c@o1039706.ingest.sentry.io/6008629",
#     integrations=[FlaskIntegration()],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0
# )


app = createApp()

if __name__ == '__main__':
    app.run(debug = True)