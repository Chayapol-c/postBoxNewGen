"use-strict"

// graph
window.onload = function () {
            const data= () =>{
                        let sumArr = ""
                        for(let i = 0 ; i < 30 ; i++){
                            sumArr += `{x: ${new Date(2021,02,i)}, y: ${i}}`
                        }
                        return sumArr
                    }
            let chart = new CanvasJS.Chart("chartContainer", {
                animationEnabled: true,
                title: {
                    text: "Supplies in one Mouth"
                },
                axisX: {
                    title: "Time",
                    valueFormatString: "DD",
                },
                axisY: {
                    title: "Piece",
                    includeZero: true,
                },
                data: [{
                    type: "line",
                    name: "CPU Utilization",
                    connectNullData: true,
                    //nullDataLineDashType: "solid",
                    dataPoints: [
                    { x: new Date(2012, 01, 1), y: 26},
                    { x: new Date(2012, 01, 3), y: 38},
                    { x: new Date(2012, 01, 5), y: 43},
                    { x: new Date(2012, 01, 7), y: 29},
                    { x: new Date(2012, 01, 11), y: 41},
                    { x: new Date(2012, 01, 13), y: 54},
                    { x: new Date(2012, 01, 20), y: 66},
                    { x: new Date(2012, 01, 21), y: 60},
                    { x: new Date(2012, 01, 25), y: 53},
                    { x: new Date(2012, 01, 27), y: 60}
                    ]
                }]
            });
            chart.render();
        }
