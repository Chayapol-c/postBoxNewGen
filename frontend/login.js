"use-strict"

const loginbtn = document.querySelector("#login--btn");

loginbtn.addEventListener("click", function(e){
    e.preventDefault()
    const username = loginbtn.closest("#user-form").querySelector("#InputUsername1").value
    const password =loginbtn.closest("#user-form").querySelector("#InputPassword1").value
    console.log(username, password)
})