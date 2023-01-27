import logging
from .BaseAnalysis import BaseAnalysis
import libcst as cst
import libcst.matchers as m
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from ..utils.nodeLocator import get_node_by_location

class LoopingAnalysis(BaseAnalysis):
    
    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(filename='output.log', format='%(message)s', level=logging.INFO)
        self.for_loop_count = 0
        self.while_loop_count = 0
        
    def begin_execution(self) -> None:
        logging.info('Starting Looping Analysis')
        
    def end_execution(self) -> None:
        logging.info('Number of for loops : {}'.format(self.for_loop_count))
        logging.info('Number of while loops : {}'.format(self.while_loop_count))
        
    def enter_for(self, dyn_ast: str, iid: int, next_value: Any) -> Optional[Any]:
        self.for_loop_count += 1
        ast, iids = self._get_ast(dyn_ast)
        target = get_node_by_location(ast, iids.iid_to_location[iid], m.For().target)
        iter = get_node_by_location(ast, iids.iid_to_location[iid], m.For().iter)
        # loop_string = cst.parse_module('').code_for_node(node).split(':')[0]
        loop_string = 'for {} in {}'.format(target, iter)
        logging.info('Entering for loop : \n{}'.format(loop_string))

    def enter_while(self, dyn_ast: str, iid: int, cond_value: bool) -> Optional[bool]:
        self.while_loop_count += 1
        ast, iids = self._get_ast(dyn_ast)
        node = get_node_by_location(ast, iids.iid_to_location[iid], m.While())
        condition = cst.parse_module('').code_for_node(node)
        logging.info('Entering while loop : \n{}'.format(condition))