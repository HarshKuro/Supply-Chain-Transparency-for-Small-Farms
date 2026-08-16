// js/firebase-config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

// TODO: Replace the following with your app's Firebase project configuration
const firebaseConfig = {

  apiKey: "AIzaSyBMfq8w9jv_iNCsk2UQc6PYQVInpB8mkN4",

  authDomain: "supply-chain-transparenc-55506.firebaseapp.com",

  projectId: "supply-chain-transparenc-55506",

  storageBucket: "supply-chain-transparenc-55506.firebasestorage.app",

  messagingSenderId: "868252957481",

  appId: "1:868252957481:web:ff384f62a0e8944582d538"

};


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };
