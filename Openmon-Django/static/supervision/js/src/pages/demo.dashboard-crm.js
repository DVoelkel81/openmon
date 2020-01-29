/**
 * Theme: Hyper - Responsive Bootstrap 4 Admin Dashboard
 * Author: Coderthemes
 * Module/App: CRM Dashboard
 */



//
// Campaign Sent Chart
//

var options1 = {
    chart: {
        type: 'bar',
        height: 60,
        sparkline: {
            enabled: true
        }
    },
    plotOptions: {
        bar: {
            columnWidth: '60%'
        }
    },
    colors: ["#727cf5"],
    series: [{
        data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54]
    }],
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    xaxis: {
        crosshairs: {
            width: 1
        },
    },
    tooltip: {
        fixed: {
            enabled: false
        },
        x: {
            show: false
        },
        y: {
            title: {
                formatter: function (seriesName) {
                    return ''
                }
            }
        },
        marker: {
            show: false
        }
    }
}

new ApexCharts(document.querySelector("#campaign-sent-chart"), options1).render();


// 
// New Leads Chart
//

var options2 = {
    chart: {
        type: 'line',
        height: 60,
        sparkline: {
            enabled: true
        }
    },
    series: [{
        data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54]
    }],
    stroke: {
        width: 2,
        curve: 'smooth'
    },
    markers: {
        size: 0
    },
    colors: ["#727cf5"],
    tooltip: {
        fixed: {
            enabled: false
        },
        x: {
            show: false
        },
        y: {
            title: {
                formatter: function (seriesName) {
                    return ''
                }
            }
        },
        marker: {
            show: false
        }
    }
}


new ApexCharts(document.querySelector("#new-leads-chart"), options2).render();


//
// Deals Charts
//

var options3 = {
    chart: {
        type: 'bar',
        height: 60,
        sparkline: {
            enabled: true
        }
    },
    plotOptions: {
        bar: {
            columnWidth: '60%'
        }
    },
    colors: ["#727cf5"],
    series: [{
        data: [12, 14, 2, 47, 42, 15, 47, 75, 65, 19, 14]
    }],
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    xaxis: {
        crosshairs: {
            width: 1
        },
    },
    tooltip: {
        fixed: {
            enabled: false
        },
        x: {
            show: false
        },
        y: {
            title: {
                formatter: function (seriesName) {
                    return ''
                }
            }
        },
        marker: {
            show: false
        }
    }
}


new ApexCharts(document.querySelector("#deals-chart"), options3).render();

//
// Booked Revenue Chart
//

var options4 = {
    chart: {
        type: 'bar',
        height: 60,
        sparkline: {
            enabled: true
        }
    },
    plotOptions: {
        bar: {
            columnWidth: '60%'
        }
    },
    colors: ["#727cf5"],
    series: [{
        data: [47, 45, 74, 14, 56, 74, 14, 11, 7, 39, 82]
    }],
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    xaxis: {
        crosshairs: {
            width: 1
        },
    },
    tooltip: {
        fixed: {
            enabled: false
        },
        x: {
            show: false
        },
        y: {
            title: {
                formatter: function (seriesName) {
                    return ''
                }
            }
        },
        marker: {
            show: false
        }
    }
}

new ApexCharts(document.querySelector("#booked-revenue-chart"), options4).render();

  
//
// CAMPAIGNS RADIALBARS CHART
//

var options = {
    chart: {
        height: 320,
        type: 'radialBar'
    },
    colors: ["#ffbc00", "#727cf5", "#0acf97"],
    series: [86, 36, 50],
    labels: ['Total Sent', 'Reached', 'Opened'],
    plotOptions: {
        radialBar: {
            track: {
                margin: 8,
            }
        }
    }
}

var chart = new ApexCharts(
    document.querySelector("#dash-campaigns-chart"),
    options
);

chart.render();


//
// REVENUE AREA CHART
//


var options = {
    chart: {
        height: 336,
        type: 'line',
        toolbar: {
            show: false
        }
    },
    stroke: {
        curve: 'smooth',
        width: 2
    },
    series: [{
        name: 'Total Revenue',
        type: 'area',
        data: [44, 55, 31, 47, 31, 43, 26, 41, 31, 47, 33, 43]
    }, {
        name: 'Total Pipeline',
        type: 'line',
        data: [55, 69, 45, 61, 43, 54, 37, 52, 44, 61, 43, 56]
    }],
    fill: {
        type: 'solid',
        opacity: [0.35, 1],
    },
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    markers: {
        size: 0
    },
    colors: ["#0acf97", "#fa5c7c"],
    yaxis: [
        {
            title: {
                text: 'Revenue (USD)',
            },
            min: 0
        }
    ],
    tooltip: {
        shared: true,
        intersect: false,
        y: {
            formatter: function (y) {
                if (typeof y !== "undefined") {
                    return y.toFixed(0) + "k";
                }
                return y;
  
            }
        }
    },
    grid: {
        borderColor: '#f1f3fa'
    },
    legend: {
        fontSize: '14px',
        fontFamily: '14px',
        offsetY: -10,
    },
    responsive: [{
        breakpoint: 600,
        options: {
            yaxis: {
                show: false
            },
            legend: {
                show: false
            }
        }
    }]
  }
  
  var chart = new ApexCharts(
    document.querySelector("#dash-revenue-chart"),
    options
  );
  
  chart.render();