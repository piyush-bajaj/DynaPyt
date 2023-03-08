from typing import Callable, Tuple, Dict
import logging
import libcst as cst
import libcst.matchers as m
from .BaseAnalysis import BaseAnalysis
from ..utils.nodeLocator import get_node_by_location, get_parent_by_type

class CallGraph(BaseAnalysis):
    def __init__(self):
        super(CallGraph, self).__init__()
        logging.basicConfig(format='%(message)s', level=logging.INFO)
        self.graph = set()

    def pre_call(self, dyn_ast: str, iid: int, function: Callable, pos_args: Tuple, kw_args: Dict):
        ast, iids = self._get_ast(dyn_ast)
        caller = get_parent_by_type(ast, iids.iid_to_location[iid], m.FunctionDef())
        callee = get_node_by_location(ast, iids.iid_to_location[iid], m.Call())
        if caller is None:
            f = 'root module'
        else:
            f = caller.name.value
        if callee is None:
            t = 'unknown'
        else:
            t = callee.func.value
        self.graph.add((f, t))
        logging.info('Added to graph')
        logging.info('Caller : {}\nTarget : {}'.format(f,t))
        logging.info('New Graph : {}'.format(self.graph))
    
    def end_execution(self):
        for element in self.graph:
            func_name = element[0]
            val = cst.Module([element[1]]).code
            print("func_name", func_name)
            print("val", val)