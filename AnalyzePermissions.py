import os
import sys
import pickle

from androguard.core.api_specific_resources import load_permission_mappings
from androguard.misc import AnalyzeAPK
from Node import Node


class AnalyzePermissions:
    def __init__(self, apk):
        a, _, self.dx = AnalyzeAPK(apk)
        self.package_dir = "L{}".format(a.get_package().replace(".", "/"))
        self.permission_list = ['android.permission.ACCESS_FINE_LOCATION',
                                'android.permission.ACCESS_COARSE_LOCATION']
        self.permission_methods = self.extract_permission_methods()
        self.limit = 15

    def extract_permission_methods(self):
        permission_methods = {}
        for permission in self.permission_list:
            for _, meth in self.dx.strings[permission].get_xref_from():
                key = "{}{}".format(meth.class_name, meth.name)
                if key not in permission_methods:
                    permission_methods[key] = set()
                permission_methods[key].add(permission)
        return permission_methods

    def update_permissions(self, node):
        for child in node.childs:
            self.update_permissions(child)
        if node.parent:
            node.parent.permissions.update(node.permissions)
    
    def terminal_nodes(self, node):
        if len(node.childs) == 0:
            return [node]
        else:
            tnodes = []
            for child in node.childs:
                tnodes += self.terminal_nodes(child)
            return tnodes
    
    def path(self, node):
        seq = []
        while node:
            seq.append(node)
            node = node.parent
        return seq

    def visit_method(self, method, node, depth):
        if depth > self.limit:
            return

        #Check permissions
        key = "{}{}".format(method.get_class_name(), method.name)
        if key in self.permission_methods:
            node.add_permissions(self.permission_methods[key])

        #Check third party
        if not node.class_name.startswith(self.package_dir):
            node.third_party()

        for class_, method_, _ in method.get_xref_to():
            if not (class_.name.startswith("Ljava/") or method_.name.startswith("log") or method_.name.startswith("<init>")):
                child = Node(class_.name, method_.name)
                node.childs.append(child)
                child.parent = node
                self.visit_method(method_, child, depth+1)

    def crawl(self):
        root_nodes = []
        for custom_class in self.dx.get_classes():
            if custom_class.name.startswith(self.package_dir):
                for method in custom_class.get_methods():
                    node = Node(custom_class.name, method.name)
                    root_nodes.append(node)
                    self.visit_method(method, node, 0)  
    
        permission_requsting_methods = {}
        for rnode in root_nodes:
            self.update_permissions(rnode)
            tnodes = self.terminal_nodes(rnode)
            for node in tnodes:
                p = self.path(node)
                if p[-1].permissions:
                    for n in reversed(p):
                        if n.permissions:
                            key = "{}{}".format(n.class_name, n.method_name)
                            permission_requsting_methods[key] = n
        return permission_requsting_methods


def run(apk):
    out = "/data/huseyinalecakir_data/CallGraphOutputs"
    analyze = AnalyzePermissions(apk)
    permission_requsting_methods = analyze.crawl()
    path = os.path.join(out, "{}.pickle".format(apk.replace(".apk", "")))
    with open(path, "wb") as target:
        pickle.dump(permission_requsting_methods, target)

"""if __name__=="__main__":
    apk = sys.argv[1]
    out = sys.argv[2]

    analyze = AnalyzePermissions(apk)
    permission_requsting_methods = analyze.crawl()

    with open(os.path.join(out, "{}.pickle".format(apk.replace(".apk", ""))), "wb") as target:
        pickle.dump(permission_requsting_methods, target)"""
