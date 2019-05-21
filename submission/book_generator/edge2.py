from artificial_idiot.search.action_book.action_book import SimpleActionBook


if __name__ == "__main__":
    name = "edge2"
    action_book = SimpleActionBook(name)
    action_book.put_action(None, ((-3, 2), (-2, 2), "MOVE"))
    action_book.put_action(None, ((-3, 1), (-2, 0), "MOVE"))
    action_book.save()
    print(f"Successfully generated: {name}")
