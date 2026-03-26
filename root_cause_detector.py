def detect_issue(file_path, ticket):

    ticket = ticket.lower()

    try:
        with open(file_path, "r", encoding="utf8", errors="ignore") as f:
            code = f.read().lower()

        # LOGIN EMAIL ISSUE
        if "login" in ticket or "email" in ticket:
            if "email" in code:
                return "Case-sensitive email comparison"

        # CART ISSUE
        if "cart" in ticket or "checkout" in ticket:
            return "Missing validation for empty cart"

        # PAYMENT ISSUE
        if "payment" in ticket:
            return "Payment status validation missing"

        # PASSWORD ISSUE
        if "password" in ticket:
            return "Password may not be hashed"

        return "Possible logical bug detected"

    except:
        return "Unable to analyze file"