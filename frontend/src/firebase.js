import { getAuth, sendSignInLinkToEmail } from "firebase/auth";
import app from "./firebaseInit"; // Import the initialized app
// import { getAnalytics } from "firebase/analytics"; // Optional: uncomment if you need Analytics
// import { getFirestore } from "firebase/firestore"; // Optional: uncomment if you need Firestore
// import { getStorage } from "firebase/storage"; // Optional: uncomment if you need Storage
// Add more imports for other Firebase services you plan to use

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
