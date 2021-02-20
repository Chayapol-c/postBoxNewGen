"use-strict";

const submitBtn = document.querySelector("#save-supply");
const table1 = document.querySelector(".table--body1");
const status = document.querySelector("#box-status");
const currUser = JSON.parse(localStorage.getItem("userData")).username;

window.addEventListener("load", function () {
  const userName = document.querySelector("#username");
  userName.textContent = currUser;

  // Get current status
  fetch(`http://158.108.182.23:3001/status?user=${currUser}`, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.Lock_postman) {
        status.style.color = "red";
      } else {
        status.style.color = "green";
        status.textContent = "Unlock";
      }
    })
    .catch((err) => console.log(err));

  genTableFromStorage();
});

const genTableFromStorage = () => {
  // Get data from server
  fetch(`http://158.108.182.23:3001/user/track?user=${currUser}`, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      if(data.result === "invalid username or mai mee track"){
        return;
      }
      data.result.forEach((row) => {
        createTable1(row.name, row.trackID, row.timestamp);
      });
    })
    .catch((err) => console.log(err));
};

const createTable1 = (name, code, time) => {
  // Create a new row and its columns
  const newRow = document.createElement("tr");
  const columnName = document.createElement("td");
  columnName.innerHTML = `${name}`;
  const columnCode = document.createElement("td");
  columnCode.innerHTML = `${code}`;
  const columnTime = document.createElement("td");
  if(time == 0){
    columnTime.innerHTML = "not delivered";
  }else{
    columnTime.innerHTML = "delivered";
  }
  const delBtn = document.createElement("button");
  delBtn.innerHTML = "delete";
  delBtn.className = "btn btn-danger";
  delBtn.classList.add("invisible");
  const columnOption = document.createElement("td");
  columnOption.appendChild(delBtn);

  // add columns into a row
  newRow.appendChild(columnName);
  newRow.appendChild(columnCode);
  newRow.appendChild(columnTime);
  newRow.appendChild(columnOption);

  // Handle mouse hover event
  newRow.addEventListener("mouseover", function () {
    const delBtn = newRow.querySelector("button");
    delBtn.classList.remove("invisible");
  });
  newRow.addEventListener("mouseout", function () {
    const delBtn = newRow.querySelector("button");
    delBtn.classList.add("invisible");
  });
  // Add a new row into table
  if ((columnName || columnCode) && columnTime.innerHTML !== "delivered") {
    table1.appendChild(newRow);
  }
};

// Delete btn handler
table1.addEventListener("click", function (e) {
  const currRow = e.target.closest("tr");
  const columns = currRow.querySelectorAll("td");
  const name = columns[0].textContent;
  const code = columns[1].textContent;
  const time = columns[2].textContent;
  const btn = columns[3].querySelector("button");
  if (e.target == btn) {
    table1.removeChild(currRow);

    // Send delete data to server
    const deleteData = {
      trackID: code
    }
    console.log(JSON.stringify(deleteData))
    fetch("http://158.108.182.23:3001/user/track", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "DELETE",
      body: JSON.stringify(deleteData),
    }).then(res => res.json())
      .then(data => console.log(data))
      .catch(err => console.log(err))

  }
});

submitBtn.addEventListener("click", function () {
  const suppliesForm = document.querySelectorAll("#floatingInput");
  const name = suppliesForm[0].value;
  const code = suppliesForm[1].value;
  suppliesForm.forEach((ele) => (ele.value = ""));
  

  // update data into server
  const storedData = {
    username: currUser,
    name: name,
    trackID: code,
  };
  fetch(`http://158.108.182.23:3001/user/track`, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(storedData),
  })
    .then((res) => res.json)
    .catch((err) => console.log(err));

  createTable1(name, code, "");
});

