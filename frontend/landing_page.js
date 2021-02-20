"use-strict";

const trackCodeBtn = document.querySelector(".submit");
const trackCode = document.querySelector("#inputTracking");
const form = document.querySelector("form");
const message = document.querySelector("#message");
const logInBtn = document.querySelector("#login-btn");
const signup = document.querySelector("#signup-btn");

trackCodeBtn.addEventListener("click", function (e) {
  const code = {
    trackID: trackCode.value,
    timestamp: Date.now()
  };
  console.log(code);
  fetch("http://158.108.182.23:3001/postman/track", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "PATCH",
    body: JSON.stringify(code),
  })
    .then((res) => res.json())
    .then((data) => console.log(data.result))
    .catch((err) => console.log(err));
  message.classList.remove("invisible");
  window.setTimeout(message.classList.add("invisible"), 2000);
});

signup.addEventListener("mouseover", function () {
  this.style.cursor = "pointer";
});

signup.addEventListener("click", function () {
  window.location.href = "signup.html";
});


form.addEventListener("submit", function (e) {
  e.preventDefault();
  const userName = e.target.children[0].children[1].value;
  const password = e.target.children[1].children[1].value;
  const userData = {
      username: userName,
      password: password
  }
  if (userName && password){
      console.log(JSON.stringify(userData))
      fetch("http://158.108.182.23:3001/login", {
          headers:{
              "Content-Type": "application/json",
          },
          method: "POST",
          body: JSON.stringify(userData),
      })
      .then(res => res.json())
      .then(data => {
          if(data.result === "login successful"){
              console.log("save to", JSON.stringify({username: userName}))
              localStorage.setItem("userData", JSON.stringify({username: userName}))
              window.location.href = "home.html"
          }
          else{
                const message = document.createElement("div");
                message.innerHTML = `${data.result}`;
                console.log(message);
                form.appendChild(message);
          }
        })
        .catch(err => console.log(err))
  }

});
