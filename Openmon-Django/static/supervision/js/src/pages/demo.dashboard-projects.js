/**
 * Theme: Hyper - Responsive Bootstrap 4 Admin Dashboard
 * Author: Coderthemes
 * Module/App: Projects Dashboard
 */



! function ($) {
    "use strict";

    var ChartJs = function () {
        this.$body = $("body"),
            this.charts = []
    };

    ChartJs.prototype.respChart = function (selector, type, data, options) {

        //default config
        Chart.defaults.global.defaultFontColor = "#8391a2";
        Chart.defaults.scale.gridLines.color = "#8391a2";

        // get selector by context
        var ctx = selector.get(0).getContext("2d");
        // pointing parent container to make chart js inherit its width
        var container = $(selector).parent();

        // this function produce the responsive Chart JS
        function generateChart() {
            // make chart width fit with its container
            var ww = selector.attr('width', $(container).width());
            var chart;
            switch (type) {
                case 'Line':
                    chart = new Chart(ctx, { type: 'line', data: data, options: options });
                    break;
                case 'Doughnut':
                    chart = new Chart(ctx, { type: 'doughnut', data: data, options: options });
                    break;
            }
            return chart;
        };
        // run function - render chart at first load
        return generateChart();
    },
        // init various charts and returns
        ChartJs.prototype.initCharts = function () {
            var charts = [];
            if ($('#task-area-chart').length > 0) {
                var lineChart = {
                  labels: [
                    "Sprint 1",
                    "Sprint 2",
                    "Sprint 3",
                    "Sprint 4",
                    "Sprint 5",
                    "Sprint 6",
                    "Sprint 7",
                    "Sprint 8",
                    "Sprint 9",
                    "Sprint 10",
                    "Sprint 11",
                    "Sprint 12",
                    "Sprint 13",
                    "Sprint 14",
                    "Sprint 15",
                    "Sprint 16",
                    "Sprint 17",
                    "Sprint 18",
                    "Sprint 19",
                    "Sprint 20",
                    "Sprint 21",
                    "Sprint 22",
                    "Sprint 23",
                    "Sprint 24"
                  ],
                  datasets: [
                    {
                      label: "This year",
                      backgroundColor:
                        "rgba(114, 124, 245, 0.3)",
                      borderColor: "#727cf5",
                      data: [
                        16,
                        44,
                        32,
                        48,
                        72,
                        60,
                        84,
                        64,
                        78,
                        50,
                        68,
                        34,
                        26,
                        44,
                        32,
                        48,
                        72,
                        60,
                        74,
                        52,
                        62,
                        50,
                        32,
                        22
                      ]
                    }
                  ]
                };

                var lineOpts = {
                    maintainAspectRatio: false,
                    legend: {
                        display: false
                    },
                    tooltips: {
                        intersect: false
                    },
                    hover: {
                        intersect: true
                    },
                    plugins: {
                        filler: {
                            propagate: false
                        }
                    },
                    scales: {
                        xAxes: [{
                            reverse: true,
                            gridLines: {
                                color: "rgba(0,0,0,0.05)"
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                stepSize: 10,
                                display: false
                            },
                            min: 10,
                            max: 100,
                            display: true,
                            borderDash: [5, 5],
                            gridLines: {
                                color: "rgba(0,0,0,0)",
                                fontColor: '#fff',
                            }
                        }]
                    }
                };
                charts.push(this.respChart($("#task-area-chart"), 'Line', lineChart, lineOpts));
            }

            if ($('#project-status-chart').length > 0) {
                //donut chart
                var donutChart = {
                    labels: [
                        "Completed",
                        "In-progress",
                        "Behind"
                    ],
                    datasets: [
                        {
                            data: [64, 26, 10],
                            backgroundColor: [
                                "#0acf97",
                                "#727cf5",
                                "#fa5c7c"
                            ],
                            borderColor: "transparent",
                            borderWidth: "3",
                        }]
                };
                var donutOpts = {
                    maintainAspectRatio: false,
                    cutoutPercentage: 80,
                    legend: {
                        display: false
                    }
                };
                charts.push(this.respChart($("#project-status-chart"), 'Doughnut', donutChart, donutOpts));
            }
            return charts;
        },
        //initializing various components and plugins
        ChartJs.prototype.init = function () {
            var $this = this;
            // font
            Chart.defaults.global.defaultFontFamily = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif';

            // init charts
            $this.charts = this.initCharts();

            // enable resizing matter
            $(window).on('resize', function (e) {
                $.each($this.charts, function (index, chart) {
                    try {
                        chart.destroy();
                    }
                    catch (err) {
                    }
                });
                $this.charts = $this.initCharts();
            });
        },

        //init flotchart
        $.ChartJs = new ChartJs, $.ChartJs.Constructor = ChartJs
}(window.jQuery),

    //initializing ChartJs
    function ($) {
        "use strict";
        $.ChartJs.init()
    }(window.jQuery);
