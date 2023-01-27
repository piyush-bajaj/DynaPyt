import logging
from .BaseAnalysis import BaseAnalysis
from types import TracebackType

class UncaughtExceptionAnalysis(BaseAnalysis):
    
    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(filename="output.log", format="%(message)s", level=logging.INFO)
        self.count = 0
        
    def uncaught_exception(self, exc: Exception, stack_trace: TracebackType) -> None:
        self.count += 1
        logging.info('Uncaught exception found')
        logging.info('Exception : ', exc)
        logging.info('Stack Trace : \n', stack_trace)
    
    def begin_execution(self) -> None:
        logging.info('Starting UncaughtException Analysis')
        
    def end_execution(self) -> None:
        if(self.count < 1):
            logging.info('There are no uncaught exception')
        else:
            logging.info('There are {} uncaught exceptions!\nPlease see the output.log for more info'.format(self.count))