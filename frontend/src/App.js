import React, { useEffect, useState } from 'react';
import './App.css';
import LandingPage from './LandingPage';
import { auth, loginUser, logoutUser } from './firebase';
import { onAuthStateChanged } from 'firebase/auth';

function App() {
  const [user, setUser] = useState(null);
  // Login form state (email, password, error) is now managed by LandingPage
  // const [email, setEmail] = useState('');
  // const [password, setPassword] = useState('');
  // const [error, setError] = useState('');

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe(); // Cleanup subscription on unmount
  }, []);

  // handleLogin is now managed by LandingPage
  // const handleLogin = async (e) => { ... };

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
        {/* LandingPage now includes the login form and manages its own layout */}
        <LandingPage loginUser={loginUser} />
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
