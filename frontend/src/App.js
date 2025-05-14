import React, { useEffect, useState } from 'react';
// import logo from './logo.svg'; // Logo no longer used directly in App.js
import './App.css';
import LandingPage from './LandingPage'; // Import the LandingPage component

function App() {
  return (
    <div className="App bg-gray-100 min-h-screen py-8">
      <LandingPage />
    </div>
  );
}

export default App;
