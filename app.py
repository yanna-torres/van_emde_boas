from clrs_20.simple import WithBTree

if __name__ == "__main__":
    print("This is the main application file.")

    tree = WithBTree(16)

    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)
    tree.insert(7)
    tree.insert(14)
    tree.insert(15)

    print(tree)

    print("Member 2:", tree.member(2))

    print(tree.root_value())

    print("Minimum:", tree.minimum())
    print("Maximum:", tree.maximum())

    print("Successor of 14:", tree.successor(14))
    print("Predecessor of 14:", tree.predecessor(14))
