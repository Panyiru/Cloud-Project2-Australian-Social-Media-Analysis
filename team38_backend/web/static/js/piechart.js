var data = genData(3);

pieOption = {
    title : {
        text: 'Tweets Sentiment Analytics',
        subtext: 'Melbourne Area',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        type: 'scroll',
        orient: 'vertical',
        right: 10,
        top: 20,
        bottom: 20,
        data: data.legendData,

        selected: data.selected
    },
    series : [
        {
            name: 'tweets sentiment',
            type: 'pie',
            radius : '55%',
            center: ['40%', '50%'],
            data: data.seriesData,
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};



function genData(count) {
    var nameList = [
        'Positive', 'Neutral', 'Negative'
    ];
    var legendData = [];
    var seriesData = [];
    var selected = {};
    for (var i = 0; i < 3; i++) {
        name = nameList[i];
        legendData.push(name);
        seriesData.push({
            name: name,
            value: Math.round(Math.random() * 1000)
        });
        selected[name] = i < 4;
    }

    return {
        legendData: legendData,
        seriesData: seriesData,
        selected: selected
    };
}
