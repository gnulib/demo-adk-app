import { initializeApp } from "firebase/app";
import { getAuth, sendSignInLinkToEmail } from "firebase/auth";
// import { getAnalytics } from "firebase/analytics"; // Optional: uncomment if you need Analytics
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

const auth = getAuth(app);

/**
 * ActionCodeSettings for email link sign-in.
 * The url field is set dynamically to the current app's origin.
 */
const actionCodeSettings = {
  url: window.location.origin,
  handleCodeInApp: true,
  iOS: {
    bundleId: 'com.example.ios'
  },
  android: {
    packageName: 'com.example.android',
    installApp: true,
    minimumVersion: '12'
  }
};

// Helper to send sign-in link to email
const sendEmailSignInLink = async (email) => {
  try {
    await sendSignInLinkToEmail(auth, email, actionCodeSettings);
    window.localStorage.setItem('emailForSignIn', email);
    // Optionally, notify the user that the link was sent
  } catch (error) {
    // Optionally, handle error
    console.error("Error sending sign-in link:", error.code, error.message);
  }
};

export default app;
export { auth, actionCodeSettings, sendEmailSignInLink };
