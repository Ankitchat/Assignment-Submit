function makechart(jsonob){
var ctx = document.getElementById("myChart").getContext("2d");
ctx.canvas.setAttribute('width', '750');
ctx.canvas.setAttribute('height', '150');
var json_obj = jsonob;
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: json_obj.dates,
        datasets: [{
            label: 'Number of Orders',
            lineTension: 0,
            borderColor: '#3BB9FF',
            data: json_obj.counts
        }]
    },
    options: {
    	responsive: true,    	
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
}

