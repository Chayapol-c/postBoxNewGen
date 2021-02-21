"use-strict";

const signup = document.querySelector("#signup");
const loginbtn = document.querySelector("#login--btn");


signup.addEventListener("mouseover", function () {
  this.style.cursor = "pointer";
});

signup.addEventListener("click", function () {
  window.location.href = "signup.html";
});

loginbtn.addEventListener("mouseover", function () {
  this.style.cursor = "pointer";
});

loginbtn.addEventListener("click", function (e) {
  e.preventDefault();
  const username = loginbtn
    .closest("#user-form")
    .querySelector("#InputUsername1").value;
  const password = loginbtn
    .closest("#user-form")
    .querySelector("#InputPassword1").value;

  const userData = {
    username: username,
    password: password,
  };

  fetch("http://158.108.182.23:3001/login", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(userData),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(`POST response: ${data.result}`);
      if (data.result === "invalid username") {
        const message = document.querySelector("#message");
        message.classList.remove("invisible")
        window.setTimeout(()=> {
          message.classList.add("invisible")
        }, 2000)
      } else {
        window.location.href = "home.html";
      }
    })
    .catch((err) => console.log(err));
});

