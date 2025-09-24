// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-app.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCGNJg_DgNY6FX2dR9RhI86e9vWMZCTC-k",
    authDomain: "hactopus-49189.firebaseapp.com",
    projectId: "hactopus-49189",
    storageBucket: "hactopus-49189.firebasestorage.app",
    messagingSenderId: "571006121738",
    appId: "1:571006121738:web:07443f87eefb25028becf3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);



const confirmPassword = document.getElementById('confirm-password').value;
const submit = document.getElementById('submit');
submit.addEventListener('click', function (event) {
    event.preventDefault();

    // inputs

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    createUserWithEmailAndPassword(getAuth(), email, password)
        .then((userCredential) => {
            // Signed in
            const user = userCredential.user;
            alert("User created successfully");
            window.location.href = "dashboard.html";
            // ...
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            alert(errorMessage);
            // ..
        });
});
// submit.addEventListener('click',()=>{
//     if(password !== confirmPassword){
//         alert("Passwords do not match");
//         return;
//     }
//     // firebase signup
//     firebase.auth().createUserWithEmailAndPassword(email, password)
//     .then((userCredential) => {
//         // Signed in
//         var user = userCredential.user;
//         alert("User created successfully");
//         window.location.href = "dashboard.html";
//         // ...
//     })
//     .catch((error) => {
//         var errorCode = error.code;
//         var errorMessage = error.message;
//         alert(errorMessage);
//         // ..
//     });
// });

