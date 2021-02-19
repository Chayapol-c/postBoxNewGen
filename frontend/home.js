"use-strict"

const submitBtn = document.querySelector("#save-supply");
const table = document.querySelector("tbody");
const status = document.querySelector("#box-status");

window.addEventListener("load", function(){
    const userName = document.querySelector("#username");
    userName.textContent = "Kaopun";
    console.log(userName);

    // Change status color
    if(status.textContent.trim() == "Lock"){
        status.style.color = "red";
    }else if (status.textContent.trim(0) == "Unlock"){
        status.style.color = "green";
    }

})

const sampleData = ["1","macbook", "adkfjoasdknglqs", "11 / 01 / 2021"];
const createTable = () => {

}

submitBtn.addEventListener("click", function(){
    const suppliesForm = document.querySelectorAll("#floatingInput")
    const name = suppliesForm[0].value;
    const code = suppliesForm[1].value;
    suppliesForm.forEach(ele => ele.value = "")
    
    // Create a new row and its columns
    const newRow = document.createElement("tr");
    const columnIndex = document.createElement("th");
    columnIndex.innerHTML = `1`;
    const columnName = document.createElement("td");
    columnName.innerHTML = `${name}`;
    const columnCode = document.createElement("td");
    columnCode.innerHTML  =`${code}`;
    const columnTime = document.createElement("td");
    // columnTime.innerHTML = `${sampleData[3]}`;
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
    newRow.addEventListener("mouseover", function(){
        const delBtn = newRow.querySelector("button");
        delBtn.classList.remove("invisible");
    })
    newRow.addEventListener("mouseout", function(){
        const delBtn = newRow.querySelector("button");
        delBtn.classList.add("invisible");
    })

    // Add a new row into table
    if(columnName  || columnCode || columnTime){
        table.appendChild(newRow);
        delBtn.addEventListener("click", function(){
            table.removeChild(newRow);
        })
    }
})
