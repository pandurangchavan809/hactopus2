// import { initializeApp } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-app.js";
// import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-auth.js";

// const firebaseConfig = {
//   apiKey: "AIzaSyCGNJg_DgNY6FX2dR9RhI86e9vWMZCTC-k",
//   authDomain: "hactopus-49189.firebaseapp.com",
//   projectId: "hactopus-49189",
//   storageBucket: "hactopus-49189.firebasestorage.app",
//   messagingSenderId: "571006121738",
//   appId: "1:571006121738:web:07443f87eefb25028becf3"
// };

// const app  = initializeApp(firebaseConfig);
// const auth = getAuth(app);

// // Display everything before the @ as the username
// onAuthStateChanged(auth, (user) => {
//   if (user && user.email) {
//     const username = user.email.split("@")[0];   // 👈 take part before @
//     const nameSpan = document.getElementById("username");
//     if (nameSpan) nameSpan.textContent = username;
//   } else {
//     // Redirect to login if no user is signed in
//     window.location.href = "login.html";
//   }
// });

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyCGNJg_DgNY6FX2dR9RhI86e9vWMZCTC-k",
  authDomain: "hactopus-49189.firebaseapp.com",
  projectId: "hactopus-49189",
  storageBucket: "hactopus-49189.firebasestorage.app",
  messagingSenderId: "571006121738",
  appId: "1:571006121738:web:07443f87eefb25028becf3"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Show username as email prefix
onAuthStateChanged(auth, (user) => {
  if (user && user.email) {
    const username = user.email.split("@")[0]; // Take part before @
    const nameSpan = document.getElementById("username");
    if (nameSpan) nameSpan.textContent = username;
  } else {
    // If no user, redirect to login
    window.location.href = "login.html";
  }
});

