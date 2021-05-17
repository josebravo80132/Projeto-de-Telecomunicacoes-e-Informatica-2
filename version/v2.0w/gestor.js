

const net = require("net");
const readline = require("readline").createInterface({
	input: process.stdin,
	output: process.stdout
});

const options = {
	host: '10.0.0.10',
	address: '0.0.0.0',
	port: 5000
};

const message = new String('0 1 10.0.16.20 10.0.15.20 1');

let gestor = net.connect(options, () =>{
	encodeURI(message);
	console.log("connected!");
})