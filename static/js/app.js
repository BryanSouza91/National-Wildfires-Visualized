
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
    Highcharts.chart('streamGraph', {

      chart: {
        type: 'streamgraph',
        marginBottom: 30,
        zoomType: 'x'
      },

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
        categories: data.streamGraph.years_categories,
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


  // console.log(D.column.sizes.map(x => x.data.size_data.reduce((a, b) => a + b, 0)))
  // console.log(D.column.sizes.map(x => x.cause))

  function buildColumnChart(data) {
    let contColSeries = [];
    data.column.days_to_cont.map(x => contColSeries.push({
      name: x.cause,
      y: x.data.cont_data.reduce((a, b) => a + b, 0),
      drilldown: x.cause
    }));
    // console.log(contColSeries);

    // let sizeColSeries = [];
    // data.column.sizes.map(x => sizeColSeries.push({
    //   name: x.cause,
    //   y: x.data.size_data.reduce((a, b) => a + b, 0),
    //   drilldown: x.cause
    // }));
    // console.log(sizeColSeries);


    let drilldownContSeries = [];
    data.column.days_to_cont.map(x => drilldownContSeries.push({
      name: x.cause,
      id: x.cause,
      data: x.data.drilldown
    }));
    // console.log(drilldownContSeries);

    // Create the chart
    Highcharts.chart('columnChart', {
      chart: {
        type: 'column'
      },
      title: {
        text: 'Days from Discovery to Containment and Area Burned'
      },
      xAxis: {
        type: 'category'
        labels: {
          align: 'left',
          reserveSpace: true,
          rotation: 315,
        }
      },
      yAxis: {
        title: "Days"
      },
      // {
      //   opposite: true,
      //   title: "Area Burned"
      // }],
      credits: {
        enabled: false
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        series: {
          borderRadius: 4,
          borderWidth: 0,
          dataLabels: {
            enabled: true,
            format: '{point.y:.0f}'
          }
        }
      },

      // tooltip: {
      //   headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      //   pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.0f}</b> days fighting fire<br/>'
      // },

      series: [
        {
          name: "Days to Contain",
          colorByPoint: true,
          data: contColSeries
        }
        // , {
        //   name: "Total Area Burned",
        //   colorByPoint: true,
        //   data: sizeColSeries
        // }
      ],
      drilldown: {
        series: drilldownContSeries
      }
    });



  };

  buildColumnChart(D);
  buildPieChart(D, st0);
  buildBarChart(D, st0);
  buildStreamGraph(D, st0);

});