import React, { useEffect, useState } from 'react';
// import logo from './logo.svg'; // Logo no longer used directly in App.js
import './App.css';
import { auth } from './firebase'; 
import LandingPage from './LandingPage'; // Import the LandingPage component
import {
  onAuthStateChanged,
  signOut
} from 'firebase/auth';

function App() {
  const [user, setUser] = useState(null);
  // const [email, setEmail] = useState(''); // Removed email state
  // const [emailSent, setEmailSent] = useState(false); // Removed emailSent state

  // Removed useEffect for handling sign-in with email link
  // useEffect(() => {
  //   if (isSignInWithEmailLink(auth, window.location.href)) {
  //     let emailForLink = window.localStorage.getItem('emailForSignIn');
  //     if (!emailForLink) {
  //       emailForLink = window.prompt('Please provide your email for confirmation');
  //     }
  //     if (emailForLink) {
  //       signInWithEmailLink(auth, emailForLink, window.location.href)
  //         .then((result) => {
  //           window.localStorage.removeItem('emailForSignIn');
  //           // setEmailSent(false); // setEmailSent is removed
  //         })
  //         .catch((error) => {
  //           console.error("Error signing in with email link:", error);
  //         });
  //     }
  //   }
  // }, []);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe();
  }, []);


  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleEmailSignIn = async (e) => {
    e.preventDefault();
    try {
      await sendEmailSignInLink(email);
      setEmailSent(true);
    } catch (error) {
      console.error("Error sending sign-in link:", error);
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  return (
    <div className="App">
      <LandingPage />
    </div>
  );
}

export default App;
