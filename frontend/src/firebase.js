import { initializeApp } from "firebase/app";
import { getAuth, signInWithEmailAndPassword, signOut } from "firebase/auth";

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

const loginUser = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    // Signed in
    // const user = userCredential.user; // user object can be accessed here if needed
    return userCredential; // Return the full userCredential
  } catch (error) {
    // const errorCode = error.code; // errorCode can be accessed here
    // const errorMessage = error.message; // errorMessage can be accessed here
    return error; // Return the error object
  }
};

const logoutUser = async () => {
  try {
    await signOut(auth);
    // Sign-out successful.
    return { success: true };
  } catch (error) {
    // An error happened.
    return error; // Return the error object
  }
};

export default app;
export { auth, loginUser, logoutUser };
