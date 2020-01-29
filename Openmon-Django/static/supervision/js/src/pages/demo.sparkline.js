/**
 * Theme: Hyper - Responsive Bootstrap 4 Admin Dashboard
 * Author: Coderthemes
 * Module/App: Sparkline Charts
 */

$( document ).ready(function() {
    
    var DrawSparkline = function() {
        $('#sparkline1').sparkline([0, 23, 43, 35, 44, 45, 56, 37, 40], {
            type: 'line',
            width: "100%",
            height: '165',
            chartRangeMax: 50,
            lineColor: '#727cf5',
            fillColor: 'rgba(114, 124, 245, 0.3)',
            highlightLineColor: 'rgba(0,0,0,.1)',
            highlightSpotColor: 'rgba(0,0,0,.2)',
            maxSpotColor:false,
            minSpotColor: false,
            spotColor:false,
            lineWidth: 1
        });

        $('#sparkline1').sparkline([25, 23, 26, 24, 25, 32, 30, 24, 19], {
            type: 'line',
            width: "100%",
            height: '165',
            chartRangeMax: 40,
            lineColor: '#0acf97',
            fillColor: 'rgba(10, 207, 151, 0.3)',
            composite: true,
            highlightLineColor: 'rgba(0,0,0,.1)',
            highlightSpotColor: 'rgba(0,0,0,.2)',
            maxSpotColor:false,
            minSpotColor: false,
            spotColor:false,
            lineWidth: 1
        });
    
        $('#sparkline2').sparkline([3, 6, 7, 8, 6, 4, 7, 10, 12, 7, 4, 9, 12, 13, 11, 12], {
            type: 'bar',
            height: '165',
            barWidth: '10',
            barSpacing: '3',
            barColor: '#39afd1'
        });
        
        $('#sparkline3').sparkline([20, 40, 30, 10], {
            type: 'pie',
            width: '165',
            height: '165',
            sliceColors: ['#39afd1','#ffbc00','#e3eaef','#fa5c7c']
        });
    
        $('#sparkline4').sparkline([0, 23, 43, 35, 44, 45, 56, 37, 40], {
            type: 'line',
            width: "100%",
            height: '165',
            chartRangeMax: 50,
            lineColor: '#ffbc00',
            fillColor: 'transparent',
            lineWidth: 2,
            highlightLineColor: 'rgba(0,0,0,.1)',
            highlightSpotColor: 'rgba(0,0,0,.2)',
            maxSpotColor:false,
            minSpotColor: false,
            spotColor:false
        });
    
        $('#sparkline4').sparkline([25, 23, 26, 24, 25, 32, 30, 24, 19], {
            type: 'line',
            width: "100%",
            height: '165',
            chartRangeMax: 40,
            lineColor: '#4eb7eb',
            fillColor: 'transparent',
            composite: true,
            lineWidth: 2,
            maxSpotColor:false,
            minSpotColor: false,
            spotColor:false,
            highlightLineColor: 'rgba(0,0,0,1)',
            highlightSpotColor: 'rgba(0,0,0,1)'
        });

        $('#sparkline6').sparkline([3, 6, 7, 8, 6, 4, 7, 10, 12, 7, 4, 9, 12, 13, 11, 12], {
            type: 'line',
            width: "100%",
            height: '165',
            lineColor: '#e3eaef',
            lineWidth: 2,
            fillColor: 'rgba(227,234,239,0.3)',
            highlightLineColor: 'rgba(0,0,0,.1)',
            highlightSpotColor: 'rgba(0,0,0,.2)'
        });

        $('#sparkline6').sparkline([3, 6, 7, 8, 6, 4, 7, 10, 12, 7, 4, 9, 12, 13, 11, 12], {
            type: 'bar',
            height: '165',
            barWidth: '10',
            barSpacing: '5',
            composite: true,
            barColor: '#6c757d'
        });

        $("#sparkline7").sparkline([4, 6, 7, 7, 4, 3, 2, 1, 4, 4, 5, 6, 3, 4, 5, 8, 7, 6, 9, 3, 2, 4, 1, 5, 6, 4, 3, 7], {
            type: 'discrete',
            width: '280',
            height: '165',
            lineColor: '#6c757d'
        });



        },
        DrawMouseSpeed = function () {
            var mrefreshinterval = 500; // update display every 500ms
            var lastmousex=-1; 
            var lastmousey=-1;
            var lastmousetime;
            var mousetravel = 0;
            var mpoints = [];
            var mpoints_max = 30;
            $('html').mousemove(function(e) {
                var mousex = e.pageX;
                var mousey = e.pageY;
                if (lastmousex > -1) {
                    mousetravel += Math.max( Math.abs(mousex-lastmousex), Math.abs(mousey-lastmousey) );
                }
                lastmousex = mousex;
                lastmousey = mousey;
            });
            var mdraw = function() {
                var md = new Date();
                var timenow = md.getTime();
                if (lastmousetime && lastmousetime!=timenow) {
                    var pps = Math.round(mousetravel / (timenow - lastmousetime) * 1000);
                    mpoints.push(pps);
                    if (mpoints.length > mpoints_max)
                        mpoints.splice(0,1);
                    mousetravel = 0;
                    $('#sparkline5').sparkline(mpoints, {
                        tooltipSuffix: ' pixels per second',
                        type: 'line',
                        width: "100%",
                        height: '165',
                        chartRangeMax: 77,
                        maxSpotColor:false,
                        minSpotColor: false,
                        spotColor:false,
                        lineWidth: 1,
                        lineColor: '#fa5c7c',
                        fillColor: 'rgba(250, 92, 124, 0.3)',
                        highlightLineColor: 'rgba(24,147,126,.1)',
                        highlightSpotColor: 'rgba(24,147,126,.2)'
                    });
                }
                lastmousetime = timenow;
                setTimeout(mdraw, mrefreshinterval);
            }
            // We could use setInterval instead, but I prefer to do it this way
            setTimeout(mdraw, mrefreshinterval); 
        };
    
    DrawSparkline();
    DrawMouseSpeed();
    
    var resizeChart;

    $(window).resize(function(e) {
        clearTimeout(resizeChart);
        resizeChart = setTimeout(function() {
            DrawSparkline();
            DrawMouseSpeed();
        }, 300);
    });
});