var config = {
    apiKey: "AIzaSyCdGTjnonOsMoMWm9DMW53wkPPCeI_vcf4",
    authDomain: "premwit-game-2019.firebaseapp.com",
    databaseURL: "https://premwit-game-2019.firebaseio.com",
    projectId: "premwit-game-2019",
    storageBucket: "premwit-game-2019.appspot.com",
    messagingSenderId: "712284503836"
};
firebase.initializeApp(config);

firebase.auth().signInWithEmailAndPassword("fuck@fuck.com", "shitshitshit").catch(function (error) {
    console.log(error);
});