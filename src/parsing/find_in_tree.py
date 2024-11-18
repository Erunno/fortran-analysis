def find_in_tree(node, class_type):
    if isinstance(node, class_type):
        return node
    
    if not hasattr(node, 'children'):
        return None
    
    for child in node.children:
        result = find_in_tree(child, class_type)
        if result:
            return result
        
def findall_in_tree(node, class_type):
    results = []
    
    if isinstance(node, class_type):
        results.append(node)
    
    if hasattr(node, 'children'):
        for child in node.children:
            results.extend(findall_in_tree(child, class_type))
    
    return results