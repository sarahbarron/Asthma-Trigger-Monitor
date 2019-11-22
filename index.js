var Blynk = require("blynk-library");

var AUTH = 'd3RuxOQXB7zoaFy2cmCreQMUALwAhReC';

var blynk = new Blynk.Blynk(AUTH);

var v1 = new blynk.VirtualPin(1);

v1.on('write', function (param) {
    console.log('V1:', param[0]);
});