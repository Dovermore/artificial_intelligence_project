from artificial_idiot.search.action_book.action_book import SimpleActionBook


name = "edge"

action_book = SimpleActionBook(name)
action_book.put_action(None, ((-3, 2), (-2, 2), "MOVE"))
action_book.put_action(None, ((-3, 0), (-3, 2), "JUMP"))
action_book.put_action(None, ((-3, 3), (-2, 3), "MOVE"))
# action_book.put_action(None, ((-3, 2), (-1, 0), "JUMP"))
# action_book.put_action(None, ((-3, 1), (-1, 1), "JUMP"))
action_book.save()

print(f"Successfully generated: {name}")
