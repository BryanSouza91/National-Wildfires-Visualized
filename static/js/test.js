
let form = document.getElementById('form');

form.addEventListener('change', function () {
  let st0_sel = document.getElementById("state0_sel");
  let st0 = st0_sel.options[st0_sel.selectedIndex].value;

  let xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", `/api/${st0}`, false); // false for synchronous request  
  xmlHttp.send(null);
  // console.log(JSON.parse(xmlHttp.responseText));
  let D = JSON.parse(xmlHttp.responseText);
  // console.log(D);

  function buildPieChart(data, st0) {
    Highcharts.chart('pieChart', {
      chart: {
        type: 'variablepie'
      },
      title: {
        text: `Number of Fires and Area Burned by Cause in ${st0}`
      },
      credits: {
        enabled: false
      },
      xAxis: {
        categories: data.column.counts.map(x => x[0])
      },
      series: [{
        name: st0,
        minPointSize: 20,
        innerSize: '25%',
        zMin: 0,
        data: data.v_pie
      }]
    });
  };

  function buildBarChart(data, st0) {
    Highcharts.chart('barChart', {
      chart: {
        type: 'bar'
      },
      title: {
        text: `Number of Fires by Cause in ${st0}`
      },
      credits: {
        enabled: false
      },
      plotOptions: {
          series: {
              borderRadius: 4,
              dataLabels: {
                  enabled: true,
                  format: '{point.y:.0f}'
              }
          }
      },
      legend: {
        enabled: false,
      },
      xAxis: {
        categories: data.column.counts.map(x => x[0])
      },
      yAxis: [{
        min: 0,
        title: {
          text: 'Counts of Fires'
        }
      }],
      series: [{
        name: 'Counts of Fires',
        data: data.column.counts
      }]
    });
  };

  function buildStreamGraph(data, st0) {
    var colors = Highcharts.getOptions().colors;
    Highcharts.chart('streamGraph', {

      chart: {
        type: 'streamgraph',
        marginBottom: 30,
        zoomType: 'x'
      },

      // Make sure connected countries have similar colors
      colors: [
        colors[0],
        colors[1],
        colors[2],
        colors[3],
        colors[4],
        colors[5],
        colors[6],
        colors[7],
        colors[8],
        colors[9],
        colors[0],
        Highcharts.color(colors[4]).brighten(0.2).get(),
        Highcharts.color(colors[7]).brighten(0.).get(),
      ],

      title: {
        floating: false,
        align: 'left',
        text: `Area Burned by Cause per Year in ${st0}`
      },

      credits: {
        enabled: false
      },

      xAxis: {
        maxPadding: 0,
        type: 'category',
        crosshair: true,
        categories: data.streamGraph.years_categories.map(x => x),
        labels: {
          align: 'left',
          reserveSpace: true,
          rotation: 315,
        },
        lineWidth: 0,
        margin: 20,
        tickWidth: 0
      },

      yAxis: {
        visible: false,
        startOnTick: false,
        endOnTick: false
      },

      legend: {
        enabled: true,
        align: 'center',
        verticalAlign: 'top',

      },
      series: data.streamGraph.data
    });
  };


  buildPieChart(D, st0);
  buildBarChart(D, st0);
  buildStreamGraph(D, st0);

});