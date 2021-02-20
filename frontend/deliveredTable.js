"use-strict"
const table =document.querySelector(".table--body2")

const genTable = () => {
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
        // createTable2(row.name, row.trackID, row.timestamp);
        createTable2(row);
      });
    })
    .catch((err) => console.log(err));
};

const createTable2 = (row) => {
  // Create a new row and its columns
  const newRow = document.createElement("tr");
  const columnName = document.createElement("td");
  columnName.innerHTML = `${row.name}`;
  const columnCode = document.createElement("td");
  columnCode.innerHTML = `${row.trackID}`;
  const columnStatus = document.createElement("td");
  if(row.timestamp == 0){
    columnStatus.innerHTML = "not delivered";
  }else{
    columnStatus.innerHTML = "delivered";
  }
  const columnTime = document.createElement("td");

  
  let date = new Date(row.timestamp)
  // create time string
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; 
  minutes = minutes < 10 ? '0'+minutes : minutes;
  let strTime = hours + ':' + minutes + ' ' + ampm;
  columnTime.innerHTML = `Day: ${date.getDate()} - ${strTime}`

  // add columns into a row
  newRow.appendChild(columnName);
  newRow.appendChild(columnCode);
  newRow.appendChild(columnStatus);
  newRow.appendChild(columnTime);

  // Add a new row into table
  if ((columnName || columnCode) && columnStatus.innerHTML === "delivered") {
    table.appendChild(newRow);
  }
};


window.addEventListener("load", function(){
    genTable();
})