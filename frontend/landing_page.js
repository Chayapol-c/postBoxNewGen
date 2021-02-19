"use-strict"

const trackCodeBtn = document.querySelector(".submit")
const trackCode = document.querySelector("#inputTracking")
const form = document.querySelector("form")


trackCodeBtn.addEventListener("click", function(e){
    console.log(trackCode.value)
});




form.addEventListener("submit", function(e){
    e.preventDefault()
    const userName = e.target.children[0].children[1].value
    const password = e.target.children[1].children[1].value

    if(userName && password){
        const message = document.createElement("div")
        message.innerHTML = "Invalid Username or Password"
        console.log(message)
        form.appendChild(message)
    }
})
