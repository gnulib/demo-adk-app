import React, { useState } from 'react';

// AcknowledgementSection removed

const IntroductionSection = () => (
  <section className="mb-8">
    <p className="text-lg md:text-xl text-gray-700 mb-4 leading-relaxed">
      This demo project showcases a simple application built with Google's ADK framework, 
      illustrating how to deploy an ADK app on Google Cloud as a Cloud Run service. 
      It also highlights the capabilities of LLMs in creating conversational interfaces for services with APIs.
    </p>
    <p className="text-lg md:text-xl text-gray-700 leading-relaxed">
      For more details, please refer to the{' '}
      <a
        href="https://github.com/gnulib/demo-adk-app/blob/main/README.md"
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:text-blue-800 font-medium underline"
      >
        project README on GitHub
      </a>.
    </p>
  </section>
);

// PowerOfLLMsSection removed

const SpecialThanksSection = () => (
  <blockquote className="mt-8 mb-6 p-6 border-l-4 border-green-500 bg-green-50 rounded-md shadow">
    <p className="text-gray-700 leading-relaxed mb-4">
      This project makes use of the excellent{' '}
      <a
        href="https://deckofcardsapi.com/"
        target="_blank"
        rel="noopener noreferrer"
        className="text-green-600 hover:text-green-800 font-medium underline"
      >
        Deck of Cards API
      </a>{' '}
      by Chase Roberts. Many thanks to Chase for providing this fun and useful API!
    </p>
    <p className="text-gray-700 leading-relaxed">
      <strong>The open and well-documented API was essential in showcasing how LLM agents can interact with real-world services with minimal effort.</strong>
    </p>
  </blockquote>
);

function LandingPage({ loginUser }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
    try {
      const result = await loginUser(email, password);
      if (result.user) {
        // User successfully logged in, App.js onAuthStateChanged will handle UI update
        setEmail('');
        setPassword('');
      } else if (result.code) {
        // Handle Firebase auth errors
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
      setError('An unexpected error occurred. Please try again.');
      console.error("Login error:", err);
    }
  };

  return (
    // Main container for the page, centered with max-width.
    // This div used to be nested inside "Landing Page Content Section".
    <div className="p-4 md:p-8 max-w-4xl mx-auto bg-white rounded-xl shadow-2xl space-y-8">
      {/* Login Form Section has been moved below the header */}

      {/* Landing Page Content Sections - now follow the login form in the same container */}
      <header className="text-center py-6">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-800">
          Demo ADK App
        </h1>
        <p className="text-lg text-gray-600 mt-2">
          Exploring Google's ADK and the Power of LLMs
        </p>
      </header>

      {/* Login Form Section - moved here, below the header */}
      <div className="w-full max-w-md mx-auto p-6 md:p-8 space-y-6 bg-gray-50 rounded-lg shadow-lg mb-12">
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

      {/* AcknowledgementSection invocation removed */}
      <IntroductionSection />
      {/* PowerOfLLMsSection invocation removed */}
      <SpecialThanksSection />
    </div>
  );
}

export default LandingPage;
