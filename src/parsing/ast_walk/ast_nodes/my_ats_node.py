from typing import Generic, TypeVar
from fparser.two.Fortran2003 import Base, Program, Assignment_Stmt, Subroutine_Stmt, Function_Stmt, Subroutine_Subprogram, Function_Subprogram, \
                                    Execution_Part, StmtBase, Call_Stmt, Name, If_Construct, Else_Stmt, Else_If_Stmt, Write_Stmt, End_If_Stmt, \
                                    Actual_Arg_Spec_List, Procedure_Designator, Part_Ref, Forall_Triplet_Spec_List, Forall_Header, \
                                    Subscript_Triplet, If_Stmt, If_Then_Stmt, Subroutine_Body, Specification_Part, End_Subroutine_Stmt, Select_Case_Stmt, \
                                    Case_Stmt, End_Select_Stmt, Case_Selector, Case_Value_Range_List, Allocation_List, Allocate_Object_List

from fparser.two.Fortran2008 import Alloc_Opt_List

from fparser.two.Fortran2008.block_nonlabel_do_construct_r814_2 import Block_Nonlabel_Do_Construct
from fparser.two.Fortran2008.loop_control_r818 import Loop_Control

from parsing.find_in_tree import find_in_node, find_in_tree

T = TypeVar('T', bound=Base)

class MyAstNode(Generic[T]):
    def __init__(self, fnode: T):
        self.fnode = fnode

class AssignmentNode(MyAstNode[Assignment_Stmt]):
    def __init__(self, fnode: Assignment_Stmt):
        super().__init__(fnode)

    def target_fnode(self):
        return self.fnode.children[0]
    
    def operator_sign(self):
        return '='
    
    def source_fnode(self):
        return self.fnode.children[2]

FunSub = TypeVar('FunSub', Subroutine_Subprogram, Function_Subprogram)
class FuncSubBaseNode(MyAstNode[FunSub]):
    def __init__(self, fnode: Subroutine_Subprogram | Function_Subprogram | Subroutine_Body):
        super().__init__(fnode)
        if isinstance(fnode, Subroutine_Body):
            self.execution_part = []
    
            if not self._fst_child_is_subroutine_second_is_specif_third_is_end(fnode):
                raise NotImplementedError("This case is not handled yet")
        
        else:
            self.execution_part: list[StmtBase] = find_in_node(fnode, Execution_Part).children

    def _fst_child_is_subroutine_second_is_specif_third_is_end(self, fnode):
        return len(fnode.children) == 3 and \
            isinstance(fnode.children[0], Subroutine_Stmt) and \
            isinstance(fnode.children[1], Specification_Part) and \
            isinstance(fnode.children[2], End_Subroutine_Stmt)
    
class SubroutineDefinitionNode(FuncSubBaseNode[Subroutine_Subprogram]):
    def __init__(self, fnode: Subroutine_Subprogram):
        super().__init__(fnode)
    
class FunctionDefinitionNode(FuncSubBaseNode[Function_Subprogram]):
    def __init__(self, fnode: Function_Subprogram):
        super().__init__(fnode)
        
class CallNode(MyAstNode[Call_Stmt]):
    def __init__(self, fnode: Call_Stmt):
        super().__init__(fnode)

        self.called_function_name = fnode.children[0].tostr().lower()

    def get_argument_expression_fnodes(self):
        arg_list = find_in_node(self.fnode, Actual_Arg_Spec_List)
        
        if arg_list is None:
            return []
        
        return arg_list.children
    
    def get_call_identifier_fnode(self):
        return self.fnode.children[0]
   
class ForLoopNode(MyAstNode[Block_Nonlabel_Do_Construct]):
    def __init__(self, fnode: Block_Nonlabel_Do_Construct):
        super().__init__(fnode)

        self.execution_part = fnode.children[1:-1]

    def do_control_fnode(self):
        # do can have no control (see Subroutine <cup> defined in [Module mod_cu_grell])
        return find_in_tree(self.fnode, Loop_Control)

class LoopControlNode(MyAstNode[Loop_Control]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

    def loop_header(self):
        return self.fnode.children[0] 

    def do_siple_do_fnodes(self):
        return self.fnode.children[1] if self.fnode.children[1] else (None, None)

class ForAllHeaderNode(MyAstNode[Forall_Header]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

    def get_triplet_fnodes(self):
        list = find_in_tree(self.fnode, Forall_Triplet_Spec_List)
        return list.children
    
class ForAllTripletNode(MyAstNode[Subscript_Triplet]):
    def __init__(self, fnode: Subscript_Triplet):
        super().__init__(fnode)
   
    def control_variable_fnode(self):
        return self.fnode.children[0]
    
    def lower_bound_fnode(self):
        return self.fnode.children[1]

    def upper_fnode(self):
        return self.fnode.children[2]
    
    def stride_fnode(self):
        return self.fnode.children[3]
    
class IfExecutionBranch:
    def __init__(self, fnode_condition: If_Construct):
        self.fnode = fnode_condition
        self.is_else_brach = isinstance(fnode_condition, Else_Stmt)
        
        self.execution_part: list[StmtBase] = []

    def add_stmt(self, stmt: StmtBase):
        self.execution_part.append(stmt)

    def condition_expr_fnode(self):
        if isinstance(self.fnode, (Else_Stmt,  If_Then_Stmt, Else_If_Stmt)):
            return self.fnode.children[0]
        elif isinstance(self.fnode.parent, If_Stmt):
            return self.fnode 
        else:
            raise NotImplementedError("This case is not handled yet")

class IfBlockNode(MyAstNode[If_Construct]):

    def __init__(self, fnode: If_Construct):
        super().__init__(fnode)
        
        self.branches: list[IfExecutionBranch] = [
            IfExecutionBranch(fnode.children[0])
        ]

        for stmt in fnode.children[1:]:
            if isinstance(stmt, Else_Stmt) or isinstance(stmt, Else_If_Stmt):
                self.branches.append(IfExecutionBranch(stmt))
                continue

            if isinstance(stmt, End_If_Stmt):
                continue

            self.branches[-1].add_stmt(stmt)
        
class WriteStdoutNode(MyAstNode[Write_Stmt]):
    def __init__(self, fnode: Write_Stmt):
        super().__init__(fnode)

class ProcedureDesignatorNode(MyAstNode[Procedure_Designator]):
    def __init__(self, fnode: Procedure_Designator):
        super().__init__(fnode)
        self.struct_variable_name = fnode.children[0].tostr().lower()
        self.property_name = fnode.children[2].tostr().lower()

    def left_ref_fnode(self):
        return self.fnode.children[0]
    
    def right_ref_fnode(self):
        return self.fnode.children[2]

class NullifyNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

    def arg_expr_fnodes(self):
        return self.fnode.children[1].children
    
class ReturnStmtNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

        # TODO: waiting for more elaborated return statement
        if not self._first_child_is_NONE(fnode):
            raise NotImplementedError("This kind of return statement is not supported yet")

    def _first_child_is_NONE(self, fnode):
        return len(fnode.children) == 1 and fnode.children[0] is None

class ExitStmtNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

    def get_exit_label(self):
        # exit can be used to escape from a loop (see Subroutine <cup> defined in [Module mod_cu_grell])
        return self.fnode.children[1]

class CycleStmtNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)
        
    def get_cycle_label(self):
        # label can be used to cycle (see Subroutine <cup> defined in [Module mod_cu_grell])
        return self.fnode.children[1]

class ContinueStmtNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

class OneCaseBranch:
    def __init__(self, fnode_condition):
        self.condition_fnode = fnode_condition
        self._execution_part = []

    def _add_stmt(self, stmt):
        self._execution_part.append(stmt)

    def execution_part(self):
        return self._execution_part
    
    def condition_expr_fnode(self):
        if self.condition_fnode.tostr().lower() == 'case default':
            return None

        case_selector = find_in_node(self.condition_fnode, Case_Selector)
        case_value_range_list = find_in_node(case_selector, Case_Value_Range_List)
        return case_value_range_list.children[0]

class CaseConstructNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

        if not isinstance(fnode.children[0], Select_Case_Stmt):
            raise NotImplementedError("This case is not handled yet")

        self._branches: list[OneCaseBranch] = []

        for stmt in fnode.children[1:]:
            if isinstance(stmt, Case_Stmt):
                self._branches.append(OneCaseBranch(stmt))
                continue

            if isinstance(stmt, End_Select_Stmt):
                continue
            
            self._branches[-1]._add_stmt(stmt)

    def select_case(self):
        return self.fnode.children[0]
    
    def cases(self) -> list[OneCaseBranch]:
        return self._branches
    
class AllocateNode(MyAstNode[Base]):
    def __init__(self, fnode):
        super().__init__(fnode)

        if not self._fst_ch_is_NONE_second_aloc_list_third_is_aloc_op_list(fnode):
            raise NotImplementedError("This case is not handled yet")

    def _fst_ch_is_NONE_second_aloc_list_third_is_aloc_op_list(self, fnode):
        return len(fnode.children) == 3 and \
            fnode.children[0] is None and \
            isinstance(fnode.children[1], Allocation_List) and \
            isinstance(fnode.children[2], Alloc_Opt_List)

    def get_allocated_fnodes(self):
        alloc_list = find_in_node(self.fnode, Allocation_List)
        return alloc_list.children
    
    def get_alloc_opt_fnodes(self):
        alloc_opt_list = find_in_node(self.fnode, Alloc_Opt_List)
        return alloc_opt_list.children

class AllocOptNode(MyAstNode[Base]):
    def __init__(self, fnode):
        super().__init__(fnode)

    def op_name(self):
        return self.fnode.children[0]
    
    def opt_expression_fnode(self):
        return self.fnode.children[1]
    
class DeallocateNode(MyAstNode[Base]):
    def __init__(self, fnode):
        super().__init__(fnode)

        if not self._fst_ch_is_alloc_list_scd_is_none(fnode):
            raise NotImplementedError("This case is not handled yet")

    def _fst_ch_is_alloc_list_scd_is_none(self, fnode):
        return len(fnode.children) == 2 and \
            isinstance(fnode.children[0], Allocate_Object_List) and \
            fnode.children[1] is None

    def get_deallocated_fnodes(self):
        alloc_list = find_in_node(self.fnode, Allocate_Object_List)
        return alloc_list.children
