
const express = require('express')
const web = express()

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
var encodedMessage = Buffer.from(message, 'utf-8');
	readline.question('Mandar mensagem de latencia?', res => {
  	console.log(`a preparar!`);
  	if(res != null){
		let gestor = net.connect(options, () =>{
			gestor.write(encodedMessage);
			console.log("Sent " + message + " to " + options.host);
		})

		gestor.on('data', (data) => {
			console.log("Recebido "+data.toString('utf-8'));
		})

		web.get('/', (req, res) => {
			res.send('Hello World!')
		})	
	}else{
		console.log('Nao recebido nada')
	}
  readline.close();
});







web.listen(3000, () => {
	console.log('Example app listening at gttp:/localhost:3000')
})
