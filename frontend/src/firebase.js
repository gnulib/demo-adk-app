// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics"; // Optional: uncomment if you need Analytics
// import { getAuth } from "firebase/auth"; // Optional: uncomment if you need Authentication
// import { getFirestore } from "firebase/firestore"; // Optional: uncomment if you need Firestore
// import { getStorage } from "firebase/storage"; // Optional: uncomment if you need Storage
// Add more imports for other Firebase services you plan to use

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID // Optional
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Optional: Initialize specific Firebase services you plan to use
// const analytics = getAnalytics(app); // Uncomment if you need Analytics
// const auth = getAuth(app); // Uncomment if you need Authentication
// const db = getFirestore(app); // Uncomment if you need Firestore
// const storage = getStorage(app); // Uncomment if you need Storage

// Export the initialized app and any services you need
export default app;
// export { auth, db, storage }; // Export services you initialized
