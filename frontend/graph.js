"use-strict";

// graph

const fetchedData = []

const getData = () => {
    const currUser = JSON.parse(localStorage.getItem("userData")).username
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
      renderGraph(data.result)
    })

    .catch((err) => console.log(err));
};

window.onload = getData()

const renderGraph = (fetchedData) => {
  // Get and managing data
  // console.log(fetchedData[0].timestamp < fetchedData[1].timestamp)

  // fetchedData.sort((a, b) => a.timestamp - b.timestamp )
  
  const data = []
  fetchedData.forEach(ele => {
    if(ele.timestamp !== 0){
      data.push({
        x: new Date(ele.timestamp),
        y: 1
      })
    }
  })
  data.sort((a,b) => a>b)
  console.log(data)
  // convert timestamp into Date

  let chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    title: {
      text: "Supplies in one Mouth",
    },
    axisX: {
      title: "Date",
      valueFormatString: "DD",
    },
    axisY: {
      title: "Pieces",
      includeZero: true,
    },
    data: [
      {
        type: "line",
        name: "CPU Utilization",
        connectNullData: true,
        //nullDataLineDashType: "solid",
        dataPoints: [
          // { x: new Date(2012, 01, 1), y: 26 },
          // { x: new Date(2012, 01, 3), y: 38 },
          // { x: new Date(2012, 01, 5), y: 43 },
          // { x: new Date(2012, 01, 7), y: 29 },
          // { x: new Date(2012, 01, 11), y: 41 },
          // { x: new Date(2012, 01, 13), y: 54 },
          // { x: new Date(2012, 01, 20), y: 66 },
          // { x: new Date(2012, 01, 21), y: 60 },
          // { x: new Date(2012, 01, 25), y: 53 },
          // { x: new Date(2012, 01, 27), y: 60 },
          ...data
        ],
      },
    ],
  });
  chart.render();
};
