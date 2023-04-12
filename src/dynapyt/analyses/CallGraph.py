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
        logging.basicConfig(filename="temp.log", format='%(message)s', level=logging.INFO)
        self.graph = {}
        self.callers = {}
        self.callees = {}

    def pre_call(self, dyn_ast: str, iid: int, function: Callable, pos_args: Tuple, kw_args: Dict):
        ast, iids = self._get_ast(dyn_ast)
        
        caller = get_parent_by_type(ast, iids.iid_to_location[iid], m.FunctionDef())
        callee = function.__qualname__
        
        key = dyn_ast.replace('.py.orig', '').replace('/','.')
        format = "file"
        
        if caller is None:
            f = 'root module'
            f = key
        else:
            caller_parent = get_parent_by_type(ast, iids.iid_to_location[iid], m.ClassDef())
            if caller_parent is None:
                f = key + '.' + caller.name.value
                format += ".func"
            else:
                f = key + '.' + caller_parent.name.value + '.' + caller.name.value
                format += ".class.func"
        if f in self.graph.keys():
            temp = self.graph[f]
            if callee not in temp:
                temp.append(callee)
                self.graph[f] = temp
                #add callee code
                temp_callees = self.callees[f]
                if hasattr(function, "__code__") : 
                    temp_callees = [function.__code__]
                else:
                    temp_callees = [function.__qualname__]
                self.callees[f] = temp_callees
            # self.graph[f] = [self.graph[f], callee]
            # self.graph[f] = [x for x in self.graph[f]]
            # self.graph[f] = self.graph[f].append(callee)
            
        else:
            self.graph[f] = [format, callee]
            if caller is None:
                self.callers[f] = [dyn_ast]
            else:
                self.callers[f] = [cst.Module([caller]).code]
            if hasattr(function, "__code__") : 
                self.callees[f] = [function.__code__]
            else:
                self.callees[f] = [function.__qualname__]
        # callee = get_node_by_location(ast, iids.iid_to_location[iid], m.Call())
        # if caller is None:
        #     f = 'root module'
        # else:
        #     f = caller.name.value
        # if callee is None:
        #     t = 'unknown'
        # else:
        #     t = callee.func.value
        # if f in self.graph.keys():
        #     self.graph[f] = [self.graph[f], t]
        # else:
        #     self.graph[f] = [t]
        # logging.info(function.__name__)
        # logging.info('Added to graph')
        # logging.info('Caller : {}\nTarget : {}'.format(f,t))
        # if dyn_ast == "/home/piyush/Documents/MT/CallGraph/flask-api/flask_api/tests/test_app.py.orig":
        #     logging.info("File : {}".format(dyn_ast))
        #     logging.info("Function Qname : {}".format(function.__qualname__))
        #     if hasattr(function, "__module__"):
        #         logging.info("Function Module: {}".format(function.__module__))

    # def end_execution(self):
    #     logging.info("Final graph")
    #     for element in self.graph:
    #         func_name = element[0]
    #         val = cst.Module([element[1]]).code
    #         logging.info("func_name", func_name)
    #         logging.info("val", val)
    
    def end_execution(self):
        # logging.info("Final graph")
        final_json = {
            "Call_Graph" : self.graph,
            "Caller" : self.callers,
            "Callee" : self.callees
        }
        logging.info("graph")
        logging.info(json.dumps(self.graph))
        logging.info("callers")
        logging.info(json.dumps(self.callers))
        logging.info("callees")
        logging.info(json.dumps(self.callees))
        # for key, value in self.graph.items():
        #     logging.info("{} : {}".format(key, value))
        # logging.info(self.graph)