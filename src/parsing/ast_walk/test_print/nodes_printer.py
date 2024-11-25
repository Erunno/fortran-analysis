from parsing.ast_walk.ast_nodes._my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, SubroutineDefinitionNode, WriteStdoutNode
from parsing.ast_walk.dispatcher import Handler, Params

class AssignmentPrinter(Handler):
    def handle(self, node: AssignmentNode , params: Params):
        print(f"Assignment Node: <{node.fnode}>")

class FunctionDefinitionPrinter(Handler):
    def handle(self, node: FunctionDefinitionNode | SubroutineDefinitionNode, params: Params):
        for stmt in node.execution_part:
            self.dispatch(node=stmt, params=params)

class CallSubroutinePrinter(Handler):
    def handle(self, node: CallNode, params: Params):
        print(f"Called: <{node.called_function_name}>")
        
class ForLoopPrinter(Handler):
    def handle(self, node: ForLoopNode, params: Params):
        print ("For Loop started")
        
        for stmt in node.execution_part:
            self.dispatch(node=stmt, params=params)

        print(f"For Loop ended")

class IfBlockPrinter(Handler):
    def handle(self, node: IfBlockNode, params: Params):
        print ("If Block started")
        
        for branch in node.branches:
            print (' -- Branch started, is else branch:', branch.is_else_brach)
            
            branch_stmts = branch.execution_part
            
            for stmt in branch_stmts:
                self.dispatch(node=stmt, params=params)
        
        print(f"If Block ended")

class WriteStdoutPrinter(Handler):
    def handle(self, node: WriteStdoutNode, params: Params):
        print(f"Write to stdout Node")