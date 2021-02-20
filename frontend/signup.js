"use-strict"
const signupbtn = document.querySelector("#signup--btn");
const login = document.querySelector("#login")

signupbtn.addEventListener("click", function(e){
    e.preventDefault()
    const username = signupbtn.closest("#user-form").querySelector("#InputUsername1").value
    const password =signupbtn.closest("#user-form").querySelector("#InputPassword1").value
    
    if (username && password){
      const userData ={
          "username": username,
          "password": password
      }
  
      fetch("http://158.108.182.23:3001/create", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(userData),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
      })
      .catch((err) => console.log(err))
      window.location.href = "landing_page.html"
    }
    

})

login.addEventListener("mouseover", function(){
  this.style.cursor= "pointer"
})

login.addEventListener("click", function(){
  window.location.href = "login.html"
})
