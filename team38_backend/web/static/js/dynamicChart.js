dOption = {
    title: {
        text: 'Real Time Sentiment Analysis',
        subtext: 'Melbourne Area'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {
                backgroundColor: '#283b56'
            }
        }
    },
    legend: {
        data:['Positive', 'Negative','Neutral','Average Sentiment']
    },
    toolbox: {
        show: true,
        feature: {
            dataView: {readOnly: false},
            restore: {},
            saveAsImage: {}
        }
    },
    dataZoom: {
        show: false,
        start: 0,
        end: 100
    },
    xAxis: [
        {
            type: 'category',
            boundaryGap: true,
            data: (function (){
                var now = new Date();
                var res = [];
                var len = 10;
                while (len--) {
                    res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
                    now = new Date(now - 2000);
                }
                return res;
            })()
        },
        // {
        //     type: 'category',
        //     boundaryGap: true,
        //     data: (function (){
        //         var now = new Date();
        //         var res = [];
        //         var len = 10;
        //         while (len--) {
        //             res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
        //             now = new Date(now - 2000);
        //         }
        //         return res;
        //     })()
        // },
        // {
        //     type: 'category',
        //     boundaryGap: true,
        //     data: (function (){
        //         var now = new Date();
        //         var res = [];
        //         var len = 10;
        //         while (len--) {
        //             res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
        //             now = new Date(now - 2000);
        //         }
        //         return res;
        //     })()
        // },
        {
            type: 'category',
            boundaryGap: true,
            data: (function (){
                var res = [];
                var len = 10;
                while (len--) {
                    res.push(10 - len - 1);
                }
                return res;
            })()
        }
    ],
    yAxis: [
        {
            type: 'value',
            scale: true,
            name: 'Positive',
            max: 1000,
            min: 0,
            boundaryGap: [0.2, 0.2]
        },
        // {
        //     type: 'value',
        //     scale: true,
        //     name: 'Negative',
        //     max: 1000,
        //     min: 0,
        //     boundaryGap: [0.2, 0.2]
        // },
        // {
        //     type: 'value',
        //     scale: true,
        //     name: 'Neutral',
        //     max: 1000,
        //     min: 0,
        //     boundaryGap: [0.2, 0.2]
        // },
        {
            type: 'value',
            scale: true,
            name: 'Average Sentiment',
            max: 1,
            min: -1,
            boundaryGap: [0.2, 0.2]
        }
    ],
    series: [
        {
            name:'Positive',
            type:'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            data:(function (){
                var res = [];
                var len = 10;
                while (len--) {
                    res.push(Math.round(Math.random() * 1000));
                }
                return res;
            })()
        },
        {
            name:'Negative',
            type:'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            data:(function (){
                var res = [];
                var len = 10;
                while (len--) {
                    res.push(Math.round(Math.random() * 1000));
                }
                return res;
            })()
        },
        {
            name:'Neutral',
            type:'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            data:(function (){
                var res = [];
                var len = 10;
                while (len--) {
                    res.push(Math.round(Math.random() * 1000));
                }
                return res;
            })()
        },
        {
            name:'Average Sentiment',
            type:'line',
            // xAxisIndex: 0,
            yAxisIndex: 1,
            data:(function (){
                var res = [];
                var len = 0;
                while (len < 10) {
                    res.push(Math.random());
                    len++;
                }
                return res;
            })()
        }
    ]
};

app.count = 11;
setInterval(function (){
    axisData = (new Date()).toLocaleTimeString().replace(/^\D*/,'');

    var data0 = dOption.series[0].data;
    var data1 = dOption.series[1].data;
    var data2 = dOption.series[2].data;
    var data3 = dOption.series[3].data;

    data0.shift();
    data0.push(Math.round(Math.random() * 1000));
    data1.shift();
    data1.push(Math.round(Math.random() * 1000));
    data2.shift();
    data2.push(Math.round(Math.random() * 1000));
    data3.shift();
    data3.push((Math.random() * 10 + 5).toFixed(1) - 0);

    dOption.xAxis[0].data.shift();
    dOption.xAxis[0].data.push(axisData);
    // dOption.xAxis[1].data.shift();
    // dOption.xAxis[1].data.push(axisData);
    // dOption.xAxis[2].data.shift();
    // dOption.xAxis[2].data.push(axisData);
    dOption.xAxis[1].data.shift();
    dOption.xAxis[1].data.push(app.count++);

    myChart.setOption(dOption);
}, 2100);
