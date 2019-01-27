const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();
const express = require('express');
const cookieParser = require('cookie-parser')();
const cors = require('cors')({origin: true});
const app = express();

const auth = (req, res, next) => {
	var token;
	if(req.headers.authorization && req.headers.authorization.startsWith('Bearer ')) {
		token = req.headers.authorization.split('Bearer ')[1];
	}else{
		console.error('No Firebase ID token was passed as a Bearer token in the Authorization header.',
        'Make sure you authorize your request by providing the following HTTP header:',
        'Authorization: Bearer <Firebase ID Token>');
		res.status(403).send('Unauthorized');
		return;
	}
	admin.auth().verifyIdToken(token)
		.then((decodedIdToken) => {
			req.user = decodedIdToken;
			return next();
		}).catch((error) => {
			console.error('Error while verifying Firebase ID token:', error);
			res.status(403).send('Unauthorized');
		});
};

app.use(cors);
app.use(auth);
app.post('/gettime', (req,res) => {
	res.send(new Date().getTime().toString());
});
const codedict = {
	'199': 2000,
	'191': 2300,
	'299': 1500,
	'292': 1500,
	'499': 1000,
	'494': 1000,
	'399': 1000,
	'699': 1000,
	'599': 505,
	'595': 1000,
	'899': 1600,
	'898': 2200,
	'911': 2500,
	'922': 2000,
	'933': 1500,
	'955': 1000,
	'988': 2800,
	'991': 100,
	'992': 100,
	'993': 100,
	'994': 100,
	'995': 100,
	'996': 100,
	'997': 100,
	'998': 100
};
app.post('/submitcode', (req,res) => {
	if(req.body.code === null || req.body.group === null || req.body.code === undefined || req.body.group == undefined){
		res.status(404).send('Code not found or group not found.');
		return;
	}
	var code = req.body.code;
	var group = parseInt(req.body.group);
	var pts = 0;
	if(code in codedict){
		pts = codedict[code] * 2000;
	}
	var ts = new Date().getTime().toString();
	admin.firestore().collection('game').doc('191qXiQdlFiXcU4HZeqz').get().then(function(doc){
		var hp0 = doc.data()['hp0'];
		var t0 = doc.data()['t0'];
		var r = doc.data()['decrement_rate'];
		var hpn = hp0 - Math.round(r*(ts - t0)/1000.0) + pts;
		admin.firestore().collection('game').doc('191qXiQdlFiXcU4HZeqz').update({
			hp0: hpn,
			t0: ts
		});
	});
	var user = req.user.uid;
	var retObj = {}
	admin.firestore().collection('logs').get().then(function(querySnapshot){
		var id = 1;
		querySnapshot.forEach(function(doc){
			var cid = doc.data()['id'];
			if(cid > id){
				id = cid;
			}
		});
		id++;
		retObj = {
			group: group,
			id: id,
			points: pts,
			timestamp: ts,
			type: 'card',
			uid: user
		};
		admin.firestore().collection('stats').where('group','==',group).get().then(function(querySnapshot){
			console.log('Size', querySnapshot.size);
			if(querySnapshot.size == 0){
				res.status(503).send('Group not found');
			}else if(querySnapshot.size > 1){
				res.status(503).send('Group duplication found');
			}else{
				querySnapshot.forEach(function(doc){
					var cpts = doc.data()['points'] + pts;
					var did = doc.id;
					admin.firestore().collection('stats').doc(did).update({
						points: cpts
					});
					admin.firestore().collection('logs').add(retObj);
					res.send('OK');
				})
			}
		})
	});
})
exports.auth = functions.region('asia-northeast1').https.onRequest(app);