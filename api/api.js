var express 		= require('express');
var bodyParser 		= require("body-parser");

// Définition des paramètres du serveur.
var hostname 		= "localhost";
var port 			= 3000;

// Création d'un objet de type Express.
var app = express();

var myRouter = express.Router();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//utilisation de CORS
app.use(function(req, res, next){
	res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
})


// Nous demandons à l'application d'utiliser notre routeur
app.use(myRouter);


// Démarrer le serveur
app.listen(port, hostname, function(){
	console.log("Mon serveur fonctionne sur http://"+ hostname +":"+port);
});
