# flake8: noqa
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    from logging import getLogger

    logger = getLogger("default")
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        error = 'Admin Command Error: %s'
        logger.error(error, ' '.join(sys.argv), exc_info=sys.exc_info())
        raise e
