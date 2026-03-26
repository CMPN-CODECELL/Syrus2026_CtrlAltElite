def generate_fix(issue):

    if issue == "Missing validation for empty cart":

        return """
// Fix: Validate cart before checkout

if(cart.length === 0){
    return res.status(400).json({
        error: "Cart is empty"
    })
}
"""

    elif issue == "Case-sensitive email comparison":

        return """
// Fix: Normalize email comparison

email = email.toLowerCase()
storedEmail = storedEmail.toLowerCase()
"""

    elif issue == "Password may not be hashed":

        return """
// Fix: Hash password before storing

const bcrypt = require('bcrypt')
password = await bcrypt.hash(password, 10)
"""

    else:

        return """
// Manual review recommended
// Root cause not clearly detected
"""