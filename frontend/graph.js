"use-strict";

// graph

const fetchedData = []

const getData = () => {
  const currUser = JSON.parse(localStorage.getItem("userData")).username
  let now = new Date();
  now = now.getMonth();
  const url = `http://158.108.182.23:3001/count?user=${currUser}&m=${now+1}`
  fetch(url, {
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
      renderGraph(data.result)
    })
    .catch((err) => console.log(err));
};


const renderGraph = (fetchedData) => {
  // Get and managing data
  
  // console.log(fetchedData)
  const data = []
  fetchedData.forEach(ele => {
    let xs = ele.split(",")
    const s = {x: Number(xs[0]), y:Number(xs[1])}
    data.push(s)
  })
  
  let chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    title: {
      text: "Supplies in one Mouth",
    },
    axisX: {
      title: "Date",
      interval:1,
    },
    axisY: {
      title: "Pieces",
      interval: 1,
      includeZero: true,
    },
    data: [
      {
        type: "line",
        name: "CPU Utilization",
        connectNullData: true,
        //nullDataLineDashType: "solid",
        dataPoints: [
          ...data
        ],
      },
    ],
  });
  window.setInterval(()=>{
    chart.render();
  }, 2000)
};

window.onload = getData()