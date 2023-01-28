import logging
from .BaseAnalysis import BaseAnalysis
import libcst as cst
import libcst.matchers as m
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from ..utils.nodeLocator import get_node_by_location

class LoopingAnalysis(BaseAnalysis):
    
    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(format='%(message)s', level=logging.INFO)
        self.for_loop_count = dict()
        self.while_loop_count = dict()

    def begin_execution(self) -> None:
        logging.info('\tStarting Looping Analysis\t')
        
    def end_execution(self) -> None:
        for key, value in self.for_loop_count.items():
            logging.info('Executed condition \t{}\t in file \t{}\t line number {} \t{}\t times'.format(key[3], key[1], key[2], value))
        for key, value in self.while_loop_count.items():
            logging.info('Executed condition \t{}\t in file \t{}\t line number {} \t{}\t times with condition value as {}'.format(key[3], key[1], key[2], value, key[4]))
        
    def enter_for(self, dyn_ast: str, iid: int, next_value: Any) -> Optional[Any]:
        ast, iids = self._get_ast(dyn_ast)
        node = get_node_by_location(ast, iids.iid_to_location[iid], m.For())        
        loc_file = self.iid_to_location(dyn_ast, iid)
        loop_string = cst.parse_module('').code_for_node(node).split(':')[0]
        # loop_string = 'for {} in {}'.format(node.target, node.iter)
        self.for_loop_count[(iid, loc_file[0], loc_file[1], loop_string)] = self.for_loop_count.get((iid, loc_file[0], loc_file[1], loop_string), 0) + 1
        logging.debug('Entering for loop : \n{}'.format(loop_string))

    def enter_while(self, dyn_ast: str, iid: int, cond_value: bool) -> Optional[bool]:
        ast, iids = self._get_ast(dyn_ast)
        node = get_node_by_location(ast, iids.iid_to_location[iid], m.While())
        loc_file = self.iid_to_location(dyn_ast, iid)
        loop_string = cst.parse_module('').code_for_node(node).split(':')[0]
        # loop_string = 'while {}'.format(node.test)
        self.while_loop_count[(iid, loc_file[0], loc_file[1], loop_string, cond_value)] = self.for_loop_count.get((iid, loc_file[0], loc_file[1], loop_string, cond_value), 0) + 1
        logging.debug('Entering while loop : \n{}'.format(loop_string))