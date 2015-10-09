import logging
import traceback

    
logger = logging.getLogger(__name__)


def skip_exception(message='<-- no message included -->', func=None):
    if func is None:
        func = logger.warning
    func('The below exception has been caught and ignored:\n%s\n%s'
         % (message, traceback.format_exc()))
            
            