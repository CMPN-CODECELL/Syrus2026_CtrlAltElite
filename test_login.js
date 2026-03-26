function login(email, storedEmail){
    if(email === storedEmail){
        return "Login success"
    }
    return "Login failed"
}