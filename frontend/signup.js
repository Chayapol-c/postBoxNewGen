"use-strict"

const signupbtn = document.querySelector("#signup--btn");

signupbtn.addEventListener("click", function(e){
    e.preventDefault()
    const username = signupbtn.closest("#user-form").querySelector("#InputUsername1").value
    const password =signupbtn.closest("#user-form").querySelector("#InputPassword1").value
    console.log(username, password)
})