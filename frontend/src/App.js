import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { auth, sendEmailSignInLink } from './firebase';
import {
  onAuthStateChanged,
  signOut,
  signInWithPopup,
  GoogleAuthProvider,
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

  const handleGoogleSignIn = async () => {
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
    } catch (error) {
      console.error("Error signing in:", error);
    }
  };

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
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {user ? (
          <div>
            <p>Welcome, {user.email}</p>
            <button onClick={handleSignOut}>Sign Out</button>
          </div>
        ) : (
          <div>
            <p>Please sign in.</p>
            <button onClick={handleGoogleSignIn}>Sign In with Google</button>
            <hr style={{ margin: '2em 0' }} />
            <form onSubmit={handleEmailSignIn} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <input
                type="email"
                value={email}
                onChange={handleEmailChange}
                placeholder="Email address"
                required
                style={{ padding: '0.5em', marginBottom: '1em' }}
              />
              <button type="submit" disabled={emailSent}>
                {emailSent ? 'Email Sent!' : 'Sign In with Email Link'}
              </button>
            </form>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
