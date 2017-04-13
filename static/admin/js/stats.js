$(function() {

    var data = [],
    series = Math.floor(Math.random() * 6) + 3;

    for (var i = 0; i < series; i++) {
        data[i] = {
            label: "Series" + (i + 1),
            data: Math.floor(Math.random() * 100) + 1
        }
    }


function euroFormatter(v, axis) {
    return v.toFixed(axis.tickDecimals) + "€";
}

});

// Morris Bar Chart
Morris.Bar({
    element: 'hero-bar',
    data: [
        {device: '1', sells: 136},
        {device: '3G', sells: 1037},
        {device: '3GS', sells: 275},
        {device: '4', sells: 380},
        {device: '4S', sells: 655},
        {device: '5', sells: 1571}
    ],
    xkey: 'device',
    ykeys: ['sells'],
    labels: ['Sells'],
    barRatio: 0.4,
    xLabelMargin: 10,
    hideHover: 'auto',
    barColors: ["#3d88ba"]
});


// Morris Donut Chart
Morris.Donut({
    element: 'hero-donut',
    data: [
        {label: 'Direct', value: 25 },
        {label: 'Referrals', value: 40 },
        {label: 'Search engines', value: 25 },
        {label: 'Unique visitors', value: 10 }
    ],
    colors: ["#30a1ec", "#76bdee", "#c4dafe"],
    formatter: function (y) { return y + "%" }
});

// Morris Donut Chart
Morris.Donut({
    element: 'hero-donut2',
    data: [
        {label: 'Google', value: 25 },
        {label: 'Yahoo', value: 40 },
        {label: 'Bing', value: 25 },
        {label: 'Yandex', value: 10 }
    ],
    colors: ["#30a1ec", "#76bdee", "#c4dafe"],
    formatter: function (y) { return y + "%" }
});


// Morris Line Chart
var tax_data = [
    {"period": "2013-04", "visits": 2407, "signups": 660},
    {"period": "2013-03", "visits": 3351, "signups": 729},
    {"period": "2013-02", "visits": 2469, "signups": 1318},
    {"period": "2013-01", "visits": 2246, "signups": 461},
    {"period": "2012-12", "visits": 3171, "signups": 1676},
    {"period": "2012-11", "visits": 2155, "signups": 681},
    {"period": "2012-10", "visits": 1226, "signups": 620},
    {"period": "2012-09", "visits": 2245, "signups": 500}
];
Morris.Line({
    element: 'hero-graph',
    data: tax_data,
    xkey: 'period',
    xLabels: "month",
    ykeys: ['visits', 'signups'],
    labels: ['Visits', 'User signups']
});



// Morris Area Chart
Morris.Area({
    element: 'hero-area',
    data: [
        {period: '2010 Q1', iphone: 2666, ipad: null, itouch: 2647},
        {period: '2010 Q2', iphone: 2778, ipad: 2294, itouch: 2441},
        {period: '2010 Q3', iphone: 4912, ipad: 1969, itouch: 2501},
        {period: '2010 Q4', iphone: 3767, ipad: 3597, itouch: 5689},
        {period: '2011 Q1', iphone: 6810, ipad: 1914, itouch: 2293},
        {period: '2011 Q2', iphone: 5670, ipad: 4293, itouch: 1881},
        {period: '2011 Q3', iphone: 4820, ipad: 3795, itouch: 1588},
        {period: '2011 Q4', iphone: 15073, ipad: 5967, itouch: 5175},
        {period: '2012 Q1', iphone: 10687, ipad: 4460, itouch: 2028},
        {period: '2012 Q2', iphone: 8432, ipad: 5713, itouch: 1791}
    ],
    xkey: 'period',
    ykeys: ['iphone', 'ipad', 'itouch'],
    labels: ['iPhone', 'iPad', 'iPod Touch'],
    lineWidth: 2,
    hideHover: 'auto',
    lineColors: ["#81d5d9", "#a6e182", "#67bdf8"]
  });



function labelFormatter(label, series) {
    return "<div style='font-size:8pt; text-align:center; padding:2px; color:white;'>" + label + "<br/>" + Math.round(series.percent) + "%</div>";
}
