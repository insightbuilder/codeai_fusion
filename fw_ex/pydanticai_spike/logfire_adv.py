from logging import basicConfig, getLogger

import logfire
import time

logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])

logger = getLogger(__name__)
# logger.error("Hello %s!", "Insight Builder")


with logfire.span("This is a span"):
    time.sleep(1)
    logfire.info("This is an info log")
    time.sleep(2)
