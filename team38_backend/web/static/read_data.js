
var sentimentJson = $.ajax({
    // url: "./data/sentiment.json",
    url: "http://115.146.85.254/per_area/",
    async: false
});

var resultJson = $.ajax({
    // url: "./data/result.json",
    url: "http://115.146.85.254/areas/",
    async: false
});

var melGeoJson = $.ajax({
    url: "./data/mel_geojson.json",
    async: false
});

// var totalJson = $.ajax({
//     url: "http://115.146.85.254/total_sentiment/",
//     async: false
// });
//
// var hourJson = $.ajax({
//     url: "http://115.146.85.254/hours/",
//     async: false
// });
//
// var weekJson = $.ajax({
//     url: "http://115.146.85.254/weekdays/",
//     async: false
// });

var rJson = JSON.parse(resultJson.responseText);
var sJson = JSON.parse(sentimentJson.responseText);
var gJson = JSON.parse(melGeoJson.responseText);
// var tJson = JSON.parse(totalJson.responseText);
// var hJson = JSON.parse(hourJson.responseText);
// var wJson = JSON.parse(weekJson.responseText);

function getMatchKeys(geoJson){
  var len = gJson["features"].length;
  var rsn_matchedKeys = [];
  // var rn_matchedKeys = [];
  for (var i=0; i<len; i++){
    var rKey = gJson["features"][i]["properties"]["SA2_MAIN16"];
    var sKey = gJson["features"][i]["properties"]["SA2_5DIG16"];
    var nKey = gJson["features"][i]["properties"]["SA2_NAME16"];
    var obj = {};
    // var bPair = {};
    // if (rKey && sKey && nKey){
      obj["rkey"] = rKey;
      obj["skey"] = sKey;
      obj["nkey"] = nKey;
    // }
    // bPair[rKey] = nKey;
    rsn_matchedKeys.push(obj);
    // rn_matchedKeys.push(bPair);
  }
  // return [rs_matchedKeys, rn_matchedKeys];
    // return [aPair, bPair];
    return rsn_matchedKeys;
}

var keyObjs = getMatchKeys(gJson);
var result_data = rJson["rows"];
var sent_data = sJson["rows"];


/* commented by wenyi
console.log(keyObjs);
console.log(result_data.length);
console.log(sent_data.length);
*/


// var neg_total = tJson["negative"]["sum"];
// var pos_total = tJson["positive"]["sum"];
// var neu_total = tJson["neutral"]["sum"];

// var pie_values = [];
// pie_values.push(neg_total, pos_total, neu_total);

// for (var h=0; h<hJson.length; h++){
//   var day_sent = (hJson[h]["sum"]/hJson[h]["count"]).toFixed(4);
//   console.log(day_sent);
// }

// console.log(keyObjs.length);

// console.log(sJson);
// console.log(rJson);
// console.log(gJson);
