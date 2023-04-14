from typing import Callable, Tuple, Dict
import logging
import libcst as cst
import libcst.matchers as m
from .BaseAnalysis import BaseAnalysis
from ..utils.nodeLocator import get_node_by_location, get_parent_by_type
import json

class CallGraph(BaseAnalysis):
    def __init__(self):
        super(CallGraph, self).__init__()
        logging.basicConfig(filename="dynapyt.json", format='%(message)s', level=logging.INFO)
        self.graph = {}

    '''
    DynaPyt hook for pre function call
    '''
    def pre_call(self, dyn_ast: str, iid: int, function: Callable, pos_args: Tuple, kw_args: Dict):
        ast, iids = self._get_ast(dyn_ast)
        
        # calling function 
        caller = get_parent_by_type(ast, iids.iid_to_location[iid], m.FunctionDef())
        # called function 
        callee = function.__qualname__
        
        #file name
        key = dyn_ast.replace('.py.orig', '').replace('/','.')
        # format = "file"
        
        if caller is None:
            f = key
        else:
            # if caller is a part of class, find the class name
            caller_parent = get_parent_by_type(ast, iids.iid_to_location[iid], m.ClassDef())
            if caller_parent is None:
                f = key + '.' + caller.name.value
                # format += ".func"
            else:
                f = key + '.' + caller_parent.name.value + '.' + caller.name.value
                # format += ".class.func"

        # if caller already added
        if f in self.graph.keys():
            temp = self.graph[f]
            # filter dupilcate callees
            if callee not in temp:
                temp.append(callee)
                self.graph[f] = temp
        else:
            # self.graph[f] = [format, callee]
            self.graph[f] = [callee]
    
    def end_execution(self):
        logging.info(json.dumps(self.graph))