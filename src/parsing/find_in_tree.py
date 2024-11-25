from fparser.two.Fortran2003 import Program, Module, Specification_Part, \
    Module_Subprogram_Part, Use_Stmt, Subroutine_Subprogram, Access_Stmt, \
    Name, Entity_Decl_List, Include_Filename, Access_Spec, Interface_Block, \
    Interface_Stmt, Function_Subprogram, Function_Stmt, Derived_Type_Def, \
    Derived_Type_Stmt, Initialization, Internal_Subprogram_Part

def _get_or_default_exclude(not_in):   
    if not_in is None:
        return []
    
    if not isinstance(not_in, list):
        return [not_in]
    
    return not_in

def find_in_tree(node, class_type, exclude=None):
    exclude =  _get_or_default_exclude(exclude)

    if isinstance(node, class_type):
        return node

    if type(node) in exclude:
        return None

    if not hasattr(node, 'children'):
        return None

    for child in node.children:
        result = find_in_tree(child, class_type, exclude)
        if result:
            return result

def findall_in_tree(node, class_type, exclude=None):
    results = []
    exclude =  _get_or_default_exclude(exclude)
    
    if isinstance(node, class_type):
        results.append(node)

    if type(node) in exclude:
        return []
    
    if hasattr(node, 'children'):
        for child in node.children:
            results.extend(findall_in_tree(child, class_type, exclude))
    
    return results

def findall_in_node(node, class_type, exclude=None):
    exclude =  _get_or_default_exclude(exclude)

    if not hasattr(node, 'children'):
        return []
    
    return [child for child in node.children if isinstance(child, class_type)]

def find_in_node(node, class_type, exclude=None):
    exclude =  _get_or_default_exclude(exclude)

    all = findall_in_node(node, class_type, exclude)

    if len(all) > 0:
        return all[0]
    