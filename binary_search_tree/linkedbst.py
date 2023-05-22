"""
File: linkedbst.py
Author: Ken Lambert
"""
import random
import time

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it'string present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root
        while True:
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)

        # return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item'string position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left == None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right == None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item'string spot
        # else:
        #     recurse(self._root)
        # self._size += 1
        node = self._root
        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            while True:
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right is None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top'string datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top'string left subtree
            #       has been removed
            # Post: top.data = maximum value in top'string left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node'string value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection'string size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0

            height_left = height1(top.left)
            height_right = height1(top.right)

            return max(height_left, height_right) + 1

        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return: bool
        '''
        nodes = self.number_of_nodes()
        return self.height() < 2*log(nodes+1)-1

    def number_of_nodes(self):
        '''
        Return number of nodes
        :return: int
        '''
        def nodes_help(root):
            if root is None:
                return 0
            left = nodes_help(root.left)
            right = nodes_help(root.right)
            return left+right+1

        return nodes_help(self._root)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        result = [elem for elem in self.inorder() if low<=elem<=high ]
        return result

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = [verticle for verticle in self.inorder()]
        self.clear()
        def help_rebalance(input_verticles):
            if input_verticles:
                mid = len(input_verticles) // 2
                return BSTNode(input_verticles[mid], help_rebalance(input_verticles[:mid]),\
                               help_rebalance(input_verticles[mid + 1:]))
        self._root = help_rebalance(nodes)
        self._size = len(nodes)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        visited = set()
        res = BSTNode(1000)
        def help_successor(root):
            if root not in visited:
                visited.add(root)
                if root.left:
                    help_successor(root.left)
                if root.right:
                    help_successor(root.right)
        help_successor(self._root)
        for node in visited:
            if node.data > item and node.data < res.data:
                res = node
        return res.data if res.data != 1000 else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        visited = set()
        res = BSTNode(-1)
        def help_predecessor(root):
            if root not in visited:
                visited.add(root)
                if root.left:
                    help_predecessor(root.left)
                if root.right:
                    help_predecessor(root.right)
        help_predecessor(self._root)
        for node in visited:
            if node.data < item and node.data > res.data:
                res = node
        return res.data if res.data != -1 else None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as file:
            words = random.sample(file.readlines(), 10000)

        lst_words = sorted(words)
        start = time.time()
        for word in words:
            lst_words.index(word)
        print(f'Time for list: {time.time() - start}')


        self.clear()
        # add 10 000 sorted words to the tree
        for word in sorted(words):
            self.add(word)
        # start to fing each word
        start = time.time()
        for word in words:
            self.find(word)
        print(f'Time for sorted tree: {time.time() - start}')


        self.clear()
        # building tree with unsorted words
        random.shuffle(words)
        for word in words:
            self.add(word)
        # start to fing each word
        start = time.time()
        random.shuffle(words)
        for word in words:
            self.find(word)
        print(f'Time for unsorted tree: {time.time() - start}')


        self.clear()
        # building tree with unsorted words
        for word in words:
            self.add(word)
        # rebalance
        self.rebalance()
        start = time.time()
        random.shuffle(words)
        for word in words:
            self.find(word)
        print(f'Time for balanced tree: {time.time() - start}')
