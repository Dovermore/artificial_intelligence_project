from artificial_idiot.search.action_book.action_book \
    import FunctionalActionBook


def can_take_piece():
    pass


if __name__ == "__main__":
    name = "edge2"
    action_book = FunctionalActionBook(name)
    action_book.put_action(None, ((-3, 0), (-2, -1), "MOVE"))
    action_book.put_action(None, ((-3, 1), (-3, 0), "MOVE"))
    action_book.put_action(None, ((-3, 2), (-2, 2), "MOVE"))
    action_book.save()
    print(f"Successfully generated: {name}")
