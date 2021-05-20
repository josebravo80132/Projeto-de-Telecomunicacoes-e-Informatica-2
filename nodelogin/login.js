var express = require('express');
var session = require('express-session');
var bodyParser = require('body-parser');
var path = require('path');
const sqlite3 = require('sqlite3').verbose();
const notes = './Projeto-de-Telecomunicacoes-e-Informatica-2/nodelogin/login.html'
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

var connection = new sqlite3.Database('localhost', (err) => {
	if (err){
		return console.error(err.message);
	}

	console.log("Connected to the localhost memory SQlite database.");
});

var app = express();
app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));
app.use(bodyParser.urlencoded({extended : true}));
app.use(bodyParser.json());
app.use(express.static(__dirname));

app.get('/', function(request, response) {
	response.sendFile(path.dirname(notes) + '/login.html')
});

app.post('/auth', function(request, response) {
	var username = request.body.username;
	var password = request.body.password;
	if (username && password) {
		connection.all('SELECT * FROM accounts WHERE username = ? AND password = ?', [username, password], function(error, results, fields) {
			if (results.length > 0) {
				request.session.loggedin = true;
				request.session.username = username;
				console.log("True")
				response.redirect('/index.html');
			} else {
				response.send('Incorrect Username and/or Password!');
				console.log("False")
			}			
			response.end();
		});
	} else {
		response.send('Please enter Username and Password!');
		response.end();
	}
});

app.post('/submit', function(request, response) {



	var teste = request.body.Teste;
	if (teste == 'Latência'){teste = 1};
	if (teste == 'Perda de Pacotes'){teste = 2};
	if (teste == 'Largura de Banda'){teste = 3};
	if (teste == 'Disponibilidade'){teste = 4};
	var peer_i = request.body.peeri;
	var peer_f = request.body.peerf;
	var opt = request.body.opt;
	var result;

	console.log(teste);
	console.log(peer_i);
	console.log(peer_f);

	const message = new String("0 "+teste+" "+peer_i+" "+peer_f+" "+opt);
	console.log(message);
	var encodedmessage = Buffer.from(message, 'utf-8');
			let gestor = net.connect(options, () =>{
				gestor.write(encodedmessage);
				console.log("Sent " + message + " to " + options.host);
			});

			gestor.on('data', (data) => {
				result  = data.toString('utf-8');
				response.send(result);
				console.log("Recebido "+data.toString('utf-8'));
			});

	//response.redirect('/resultado')
});

app.get('/resultado', function(request, response){
	connection.all('SELECT  FROM TESTES', function(err, data, fields){
		if (err) throw err;
		response.send(data);
		console.log(data[0].RESULT);
	});
	

});

app.get('/resultados', function(request, response) {
	connection.all('SELECT * FROM TESTES', function(err, data, fields){
		if (err) throw err;
		response.send(data);
		console.log(data[0].RESULT);
	});
});

app.listen(3000);