
var revs = [];
var edus = [];
var ages = [];
var chis = [];
var vols = [];
var sents = [];
var names = [];

var keys = [];
for (var i=0; i<keyObjs.length; i++){
  var obj = keyObjs[i];
  var rKey = obj.rkey;
  var sKey = obj.skey;
  var nKey = obj.nkey;
  keys.push(rKey);
  keys.push(sKey);
  keys.push(nKey);
}

for (var s=0; s<sent_data.length; s++){
  var skey = sent_data[s]["key"];
  for(var r=0; r<keys.length; r++){
    if (keys[r] == skey){
      sent_data[s]["key"] = keys[r-1];
    }
  }
}
console.log(sent_data);

for (var j=0; j<result_data.length; j++){
  var rkey = result_data[j]["key"];
  var rev = result_data[j]["value"]["average_income_per_person_per_week"];
  var edu = result_data[j]["value"]["higher_education_percentage"];
  var age = result_data[j]["value"]["medium_age"];
  var chi = result_data[j]["value"]["having_children_percentage"];
  var vol = result_data[j]["value"]["volunteer_total_num"];
  revs.push(rev);
  edus.push(edu);
  ages.push(age);
  chis.push(chi);
  vols.push(vol);

  function matchKey(rkey){
    for(var s=0; s<sent_data.length; s++){
      var skey = sent_data[s]["key"];
        if(skey == rkey){
          return true;
        }
      }
    return false;
  }

  var match = matchKey(rkey);
  if(match){
    for(var s=0; s<sent_data.length; s++){
      var skey = sent_data[s]["key"];
        if(skey == rkey){
          var sum = sent_data[s]["value"]["sum"];
          var count = sent_data[s]["value"]["count"];
          var sent = (sum/count).toFixed(4);
          sents.push(sent);
          console.log(sent);
        }
    }
  }
  else{
    sents.push(0);
    console.log(sent);
  }

  // for(var s=0; s<sent_data.length; s++){
  //   var skey = sent_data[s]["key"];
  //     if(skey == rkey){
  //       var sum = sent_data[s]["value"]["sum"];
  //       var count = sent_data[s]["value"]["count"];
  //       var sent = (sum/count).toFixed(4);
  //       sents.push(sent);
  //       console.log(sent);
  //     }
  // }

  for(var r=0; r<keys.length; r++){
      if(keys[r] == rkey){
        names.push(keys[r+2]);;
      }
  }

}


// console.log(sents);
// console.log(names);

// for (var k=0; k<sent_data.length; k++){
//     var sum = sent_data[k]["value"]["sum"];
//     var count = sent_data[k]["value"]["count"];
//     var sent = (sum/count).toFixed(4);
//     sents.push(sent);
//   }

// console.log(revs);
// console.log(edus);
// console.log(chis);
// console.log(ages);
// console.log(vols);
// console.log(sents);

var trace1 = {
  x: revs,
  y: sents,
  mode: 'markers+text',
  type: 'scatter',
  name: 'Team A',
  // text: names,
  textposition: 'top center',
  textfont: {
    family:  'Raleway, sans-serif'
  },
  marker: { size: 8 }
};

var scatter_data1 = [ trace1 ];

var scatter_layout1 = {
  xaxis: {
    title:"Income($)",
    range: [ 200, 1800 ]
  },
  yaxis: {
    title:"Tweet Sentiment Polarity",
    range: [-1, 1]
  },
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
  title:'Scatter Plot - Sentiment by Avg Income per Person per Week'
};

var trace2 = {
  x: ages,
  y: sents,
  mode: 'markers+text',
  type: 'scatter',
  name: 'Team A',
  // text: names,
  textposition: 'top center',
  textfont: {
    family:  'Raleway, sans-serif'
  },
  marker: { size: 8 }
};

var scatter_data2 = [ trace2 ];

var scatter_layout2 = {
  xaxis: {
    title: "Age(y/o)",
    range: [ 1, 100 ]
  },
  yaxis: {
    title:"Tweet Sentiment Polarity",
    range: [-1, 1]
  },
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
  title:'Scatter Plot - Sentiment by Medium Age'
};

var trace3 = {
  x: edus,
  y: sents,
  mode: 'markers+text',
  type: 'scatter',
  name: 'Team A',
  // text: names,
  textposition: 'top center',
  textfont: {
    family:  'Raleway, sans-serif'
  },
  marker: { size: 8 }
};

var scatter_data3 = [ trace3 ];

var scatter_layout3 = {
  xaxis: {
    title: "Percentage(%)",
    range: [ 1, 100 ]
  },
  yaxis: {
    title:"Tweet Sentiment Polarity",
    range: [-1, 1]
  },
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
  title:'Scatter Plot - Sentiment by Higher Education Percentage'
};

var trace4 = {
  x: chis,
  y: sents,
  mode: 'markers+text',
  type: 'scatter',
  name: 'Team A',
  // text: names,
  textposition: 'top center',
  textfont: {
    family:  'Raleway, sans-serif'
  },
  marker: { size: 8 }
};

var scatter_data4 = [ trace4 ];

var scatter_layout4 = {
  xaxis: {
    title: "Percentage(%)",
    range: [ 1, 100 ]
  },
  yaxis: {
    title:"Tweet Sentiment Polarity",
    range: [-1, 1]
  },
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
  title:'Scatter Plot - Sentiment by Living with Children Percentage'
};

var trace5 = {
  x: vols,
  y: sents,
  mode: 'markers+text',
  type: 'scatter',
  name: 'Team A',
  // text: names,
  textposition: 'top center',
  textfont: {
    family:  'Raleway, sans-serif'
  },
  marker: { size: 8 }
};

var scatter_data5 = [ trace5 ];

var scatter_layout5 = {
  xaxis: {
    title:"Volunteers(#)",
    range: [ 0, 6000 ]
  },
  yaxis: {
    title:"Tweet Sentiment Polarity",
    range: [-1, 1]
  },
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
  title:'Scatter Plot - Sentiment by Volunteer Total Number'
};

Plotly.newPlot('scatter_chart1', scatter_data1, scatter_layout1);
Plotly.newPlot('scatter_chart2', scatter_data2, scatter_layout2);
Plotly.newPlot('scatter_chart3', scatter_data3, scatter_layout3);
Plotly.newPlot('scatter_chart4', scatter_data4, scatter_layout4);
Plotly.newPlot('scatter_chart5', scatter_data5, scatter_layout5);
