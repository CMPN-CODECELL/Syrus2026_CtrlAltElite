def ai_reasoning(ticket, code):

    ticket = ticket.lower()
    code = code.lower()

    match_score = 0
    root_cause = ""
    fix = ""
    explanation = ""

    # CART
    if "cart" in ticket:
        match_score += 2
        if "cart" in code:
            match_score += 2

        root_cause = "Cart is not validated before checkout."
        fix = """if(cart.length === 0){
    return res.status(400).json({error:"Cart is empty"})
}"""
        explanation = "Detected missing cart validation before checkout."

    # LOGIN
    elif "login" in ticket or "email" in ticket:
        match_score += 2
        if "email" in code:
            match_score += 2

        root_cause = "Email comparison is case-sensitive."
        fix = """email = email.toLowerCase()
storedEmail = storedEmail.toLowerCase()"""
        explanation = "Uppercase email mismatch causes login failure."

    # PAYMENT
    elif "payment" in ticket:
        match_score += 2
        if "payment" in code:
            match_score += 2

        root_cause = "Payment status is not validated."
        fix = """if(payment.status !== "success"){
    return res.status(400).json({error:"Payment failed"})
}"""
        explanation = "Missing payment success validation."

    # ORDER
    elif "order" in ticket:
        match_score += 2
        if "order" in code:
            match_score += 2

        root_cause = "Order validation missing."
        fix = """if(!order){
    return res.status(404).json({error:"Order not found"})
}"""
        explanation = "Order existence not checked."

    # PASSWORD
    elif "password" in ticket:
        match_score += 2
        if "password" in code:
            match_score += 2

        root_cause = "Password stored without hashing."
        fix = """const bcrypt = require('bcrypt')
password = await bcrypt.hash(password, 10)"""
        explanation = "Password should be hashed before storing."

    else:
        match_score = 1
        root_cause = "Generic issue detected."
        fix = "// Add validation"
        explanation = "Fallback reasoning."

    # 🔥 CONFIDENCE CALCULATION
    if match_score >= 4:
        confidence = 0.90
        risk = "Low"
    elif match_score == 3:
        confidence = 0.80
        risk = "Low"
    elif match_score == 2:
        confidence = 0.70
        risk = "Medium"
    else:
        confidence = 0.60
        risk = "High"

    return {
        "root_cause": root_cause,
        "fix": fix,
        "confidence": confidence,
        "risk": risk,
        "explanation": explanation
    }