import React, { useEffect, useState } from 'react';
import './App.css';
import LandingPage from './LandingPage';
import { auth, loginUser, logoutUser } from './firebase';
import { onAuthStateChanged } from 'firebase/auth';

function App() {
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe(); // Cleanup subscription on unmount
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
    try {
      const result = await loginUser(email, password);
      if (result.user) {
        // User successfully logged in, onAuthStateChanged will update the user state
        setEmail('');
        setPassword('');
      } else if (result.code) {
        // Handle Firebase auth errors (e.g., auth/wrong-password, auth/user-not-found)
        switch (result.code) {
          case 'auth/user-not-found':
            setError('No user found with this email.');
            break;
          case 'auth/wrong-password':
            setError('Incorrect password. Please try again.');
            break;
          case 'auth/invalid-email':
            setError('Invalid email format.');
            break;
          default:
            setError('Failed to login. Please check your credentials.');
        }
      }
    } catch (err) {
      // Catch any other unexpected errors
      setError('An unexpected error occurred. Please try again.');
      console.error("Login error:", err);
    }
  };

  const handleLogout = async () => {
    try {
      await logoutUser();
      // onAuthStateChanged will set user to null
    } catch (err) {
      console.error("Logout error:", err);
      setError('Failed to logout.');
    }
  };

  if (!user) {
    return (
      <div className="App bg-gray-100 min-h-screen py-8 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:space-x-8 items-start max-w-7xl mx-auto">
          {/* Login Form Section */}
          <div className="w-full md:w-1/3 lg:w-1/4 p-6 md:p-8 space-y-6 bg-white rounded-lg shadow-xl mb-8 md:mb-0 md:sticky md:top-8">
            <h2 className="text-2xl font-bold text-center text-gray-900">Login</h2>
            <form onSubmit={handleLogin} className="space-y-6">
              <div>
                <label htmlFor="email-address" className="sr-only">Email address</label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">Password</label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              {error && <p className="text-sm text-red-600 text-center">{error}</p>}
              <div>
                <button
                  type="submit"
                  className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Sign in
                </button>
              </div>
            </form>
          </div>
          {/* Landing Page Section */}
          <div className="w-full md:w-2/3 lg:w-3/4">
            <LandingPage />
          </div>
        </div>
      </div>
    );
  }

  // User is logged in
  return (
    <div className="App bg-gray-100 min-h-screen py-8 flex flex-col items-center justify-center">
      <div className="w-full max-w-2xl p-8 space-y-6 bg-white rounded-lg shadow-xl text-center">
        <h1 className="text-3xl font-bold text-gray-800">App Canvas</h1>
        <p className="text-xl text-gray-600">Welcome, <span className="font-semibold">{user.email}</span>!</p>
        <p className="text-md text-gray-500">User ID: {user.uid}</p>
        {/* Placeholder for actual app functionality */}
        <div className="mt-6 p-10 bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg">
          <p className="text-gray-400">Your application content will go here.</p>
        </div>
        <button
          onClick={handleLogout}
          className="mt-8 group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          Sign Out
        </button>
      </div>
    </div>
  );
}

export default App;
