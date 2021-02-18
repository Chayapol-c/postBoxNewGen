"use-strict"

const userName = document.querySelector("#username")
const submitBtn = document.querySelector("#save-supply")
const table = document.querySelector("tbody")


submitBtn.addEventListener("click", function(){
    const suppliesForm = document.querySelectorAll("#floatingInput")
    const name = suppliesForm[0].value;
    const code = suppliesForm[1].value;
    suppliesForm.forEach(ele => ele.value = "")
    
    const newRow = document.createElement("tr")
    const columnIndex = document.createElement("th")
    columnIndex.innerHTML = `1`
    const columnName = document.createElement("td")
    columnName.innerHTML = `${name}`
    const columnCode = document.createElement("td")
    columnCode.innerHTML  =`${code}`
    const columnTime = document.createElement("td")
    columnTime.innerHTML = `01 / 01 / 2021`

    newRow.appendChild(columnIndex)
    newRow.appendChild(columnName)
    newRow.appendChild(columnCode)
    newRow.appendChild(columnTime)
    console.log(newRow)

    table.appendChild(newRow)
})
