import streamlit as st
import graphviz

# === BST Node Definition ===
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# === BST Class ===
class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        def _insert(root, key):
            if root is None:
                return Node(key)
            if key < root.key:
                root.left = _insert(root.left, key)
            elif key > root.key:
                root.right = _insert(root.right, key)
            return root
        self.root = _insert(self.root, key)

    def delete(self, key):
        def _min_value_node(node):
            current = node
            while current.left:
                current = current.left
            return current

        def _delete(root, key):
            if root is None:
                return root
            if key < root.key:
                root.left = _delete(root.left, key)
            elif key > root.key:
                root.right = _delete(root.right, key)
            else:
                if root.left is None:
                    return root.right
                elif root.right is None:
                    return root.left
                temp = _min_value_node(root.right)
                root.key = temp.key
                root.right = _delete(root.right, temp.key)
            return root
        self.root = _delete(self.root, key)

    def visualize(self):
        def add_nodes_edges(dot, node):
            if node:
                if node.left:
                    dot.edge(str(node.key), str(node.left.key))
                    add_nodes_edges(dot, node.left)
                if node.right:
                    dot.edge(str(node.key), str(node.right.key))
                    add_nodes_edges(dot, node.right)

        dot = graphviz.Digraph()
        if self.root:
            dot.node(str(self.root.key))
            add_nodes_edges(dot, self.root)
        return dot

    def inorder(self):
        def _inorder(node):
            return _inorder(node.left) + [node.key] + _inorder(node.right) if node else []
        return _inorder(self.root)

# === Streamlit UI ===
st.title("Binary Search Tree Visualizer")

# Create or reuse BST instance in session state
if "bst" not in st.session_state:
    st.session_state.bst = BST()

# Input for adding and deleting nodes
add_val = st.number_input("Add node:", value=0, step=1)
if st.button("Insert"):
    st.session_state.bst.insert(add_val)
    st.success(f"Inserted {add_val}")

del_val = st.number_input("Delete node:", value=0, step=1, key="delete")
if st.button("Delete"):
    st.session_state.bst.delete(del_val)
    st.warning(f"Deleted {del_val}")

# Show BST structure
st.subheader("Inorder Traversal (sorted):")
st.code(" -> ".join(map(str, st.session_state.bst.inorder())) or "Tree is empty")

# Show visual representation
st.subheader("Tree Structure")
dot = st.session_state.bst.visualize()
st.graphviz_chart(dot)
