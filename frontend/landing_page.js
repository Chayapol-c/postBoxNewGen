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
  };
  console.log(JSON.stringify(code));
  fetch("http://158.108.182.23:3001/postman/track", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "PATCH",
    body: JSON.stringify(code),
  })
    .then((res) => res.json())
    .then((data) => {

      console.log(data.result)
      message.classList.remove("invisible");
      if (trackCode.value) {
        message.innerHTML = data.result ;
      } else {
        message.innerHTML = "input code";
      }
      window.setTimeout(() => {
        message.classList.add("invisible");
      }, 4000);
      trackCode.value = "";

    })
    .catch((err) => console.log(err));

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
    password: password,
  };
  if (userName && password) {
    fetch("http://158.108.182.23:3001/login", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(userData),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.result === "login successful") {
          console.log("save to", JSON.stringify({ username: userName }));
          localStorage.setItem(
            "userData",
            JSON.stringify({ username: userName })
          );
          window.location.href = "home.html";
        } else {
          const message = document.createElement("div");
          message.innerHTML = "Invalid username or password";
          message.classList = " text-danger position-absolute";
          message.style.fontWeight = "600";
          message.style.backgroundColor = "rgba(255,255,255,0.7)";
          message.style.bottom ="0";
          form.appendChild(message);
          window.setTimeout(() => {
            form.removeChild(message);
          }, 2000);
        }
      })
      .catch((err) => console.log(err));
  }
});
