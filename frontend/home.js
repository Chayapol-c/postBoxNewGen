"use-strict";

const submitBtn = document.querySelector("#save-supply");
const table = document.querySelector("tbody");
const status = document.querySelector("#box-status");

window.addEventListener("load", function () {
  const userName = document.querySelector("#username");
  userName.textContent = "Kaopun";
  // Change status color
  if (status.textContent.trim() == "Lock") {
    status.style.color = "red";
  } else if (status.textContent.trim(0) == "Unlock") {
    status.style.color = "green";
  }
  genTableFromStorage();
});

const genTableFromStorage = () => {
  const data = JSON.parse(localStorage.getItem("userDetail"));
  if (data) {
    const reData = [];
    data.forEach((row) => {
      const name = row.localSupplyName;
      const code = row.localSupplyCode;
      const time = row.localSupplyTime;
      reData.push([name, code, time]);
      createTable(name, code, time);
    });
  }
};

const createTable = (name, code, time) => {
  // Create a new row and its columns
  const newRow = document.createElement("tr");
  const columnIndex = document.createElement("th");
  columnIndex.innerHTML = `1`;
  const columnName = document.createElement("td");
  columnName.innerHTML = `${name}`;
  const columnCode = document.createElement("td");
  columnCode.innerHTML = `${code}`;
  const columnTime = document.createElement("td");
  columnTime.innerHTML = `${time}`;
  const delBtn = document.createElement("button");
  delBtn.innerHTML = "delete";
  delBtn.className = "btn btn-danger";
  delBtn.classList.add("invisible");
  const columnOption = document.createElement("td");
  columnOption.appendChild(delBtn);

  // add columns into a row
  newRow.appendChild(columnIndex);
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
  if (columnName || columnCode || columnTime) {
    table.appendChild(newRow);
  }
};

// Delete btn handler
table.addEventListener("click", function (e) {
  const currRow = e.target.closest("tr");
  const columns = currRow.querySelectorAll("td");
  const name = columns[0].textContent;
  const code = columns[1].textContent;
  const time = columns[2].textContent;
  const btn = columns[3].querySelector("button");
  if (e.target == btn) {
    table.removeChild(currRow);
    const delData = JSON.parse(localStorage.getItem("userDetail"));
    delData.map((ele, index) => {
      if (
        ele.localSupplyName === name &&
        ele.localSupplyCode === code &&
        ele.localSupplyTime === time
      ) {
        delData.splice(index, 1);
        console.log("delete one")
      }
    });
    localStorage.setItem("userDetail", JSON.stringify(delData));
  }
});

submitBtn.addEventListener("click", function () {
  const suppliesForm = document.querySelectorAll("#floatingInput");
  const name = suppliesForm[0].value;
  const code = suppliesForm[1].value;
  suppliesForm.forEach((ele) => (ele.value = ""));

  // make data store into object
  const storedData = {
    localSupplyName: name,
    localSupplyCode: code,
    localSupplyTime: "some time",
  };

  // update data into local storage
  const oldData = JSON.parse(localStorage.getItem("userDetail"));
  if (!oldData) {
    localStorage.setItem("userDetail", JSON.stringify([storedData]));
  } else {
    oldData.push(storedData);
    localStorage.setItem("userDetail", JSON.stringify(oldData));
  }
  createTable(name, code, "");
});

//Sending data back
fetch("http://127.0.0.1:5501/frontend/home.html", {
  headers: {
    "Content-Type": "application/json",
  },
  method: "POST",

  body: JSON.stringify({ data: "testdata" }),
})
  .then((res) => res.text())
  .then((text) => console.log(`POST response: ${text}`))
  .catch((err) => console.log(err));
