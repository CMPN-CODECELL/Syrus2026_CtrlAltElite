def parse_ticket(ticket):

    keywords = []

    possible_words = [
        "login",
        "auth",
        "cart",
        "checkout",
        "payment",
        "order",
        "user"
    ]

    ticket = ticket.lower()

    for word in possible_words:
        if word in ticket:
            keywords.append(word)

    return keywords