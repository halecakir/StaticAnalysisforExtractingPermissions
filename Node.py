class Node:
    def __init__(self, class_name, method_name):
        self.class_name = class_name
        self.method_name = method_name
        self.childs = []
        self.parent = None
        self.permissions = set()
        self.is_third_party = False

    def add_child(self, node):
        node.parent = self
        self.childs.append(node)

    def third_party(self):
        self.is_third_party = True

    def add_permissions(self, permissions):
        self.permissions.update(permissions)
