import React, { useEffect, useState } from 'react';
// import logo from './logo.svg'; // Logo no longer used directly in App.js
import './App.css';
import { auth, sendEmailSignInLink } from './firebase'; // sendEmailSignInLink might be unused now
import LandingPage from './LandingPage'; // Import the LandingPage component
import {
  onAuthStateChanged,
  signOut,
  isSignInWithEmailLink,
  signInWithEmailLink
} from 'firebase/auth';

function App() {
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [emailSent, setEmailSent] = useState(false);

  // Handle sign-in with email link if present in URL
  useEffect(() => {
    if (isSignInWithEmailLink(auth, window.location.href)) {
      let emailForLink = window.localStorage.getItem('emailForSignIn');
      if (!emailForLink) {
        emailForLink = window.prompt('Please provide your email for confirmation');
      }
      if (emailForLink) {
        signInWithEmailLink(auth, emailForLink, window.location.href)
          .then((result) => {
            window.localStorage.removeItem('emailForSignIn');
            setEmailSent(false);
          })
          .catch((error) => {
            console.error("Error signing in with email link:", error);
          });
      }
    }
  }, []);

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
