import React from 'react';

const AcknowledgementSection = () => (
  <blockquote className="mb-6 p-6 border-l-4 border-blue-500 bg-blue-50 rounded-md shadow">
    <p className="text-lg font-semibold text-blue-800 mb-2">Acknowledgement</p>
    <p className="text-gray-700 leading-relaxed">
      This project makes use of the excellent{' '}
      <a
        href="https://deckofcardsapi.com/"
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:text-blue-800 font-medium underline"
      >
        Deck of Cards API
      </a>{' '}
      by Chase Roberts. Many thanks to Chase for providing this fun and useful API!
    </p>
  </blockquote>
);

const IntroductionSection = () => (
  <section className="mb-8">
    <p className="text-lg md:text-xl text-gray-700 mb-4 leading-relaxed">
      This is a demo project for a simple app using{' '}
      <a
        href="https://google.github.io/adk-docs/"
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:text-blue-800 font-medium underline"
      >
        Google's ADK
      </a>{' '}
      framework. This project is intended to demonstrate how to setup a GCP project for deploying ADK app as a cloud run service.
    </p>
    <p className="text-lg md:text-xl text-gray-700 leading-relaxed">
      Secondary objective of this project is to demonstrate the power of LLMs, how they can be used to build conversation interface against pretty much any service that has reasonable APIs.
    </p>
  </section>
);

const PowerOfLLMsSection = () => (
  <section className="mb-8 p-6 bg-white rounded-lg shadow-lg">
    <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">The Power of LLM-based Agents as Middleware</h2>
    <p className="text-lg text-gray-700 mb-6 leading-relaxed">
      This project, while simple in functionality, demonstrates the remarkable power of Large Language Models (LLMs) as middleware for backend services. The agent in this demo is able to:
    </p>
    <ul className="space-y-4 mb-6">
      {[
        {
          title: "Understand API Capabilities from Docstrings",
          text: "The agent uses the docstrings of simple Python wrapper functions to understand what each API call does. No additional schema, OpenAPI spec, or manual translation is required—just clear function docstrings."
        },
        {
          title: "Interpret API Responses Directly",
          text: "The agent can read and reason about the raw API responses (typically JSON), extracting the information it needs without any custom parsing or mapping logic."
        },
        {
          title: "Autonomously Orchestrate Workflows",
          text: "Given a user request, the agent can decide which API(s) to call, in what order, and how to use the results—without any hardcoded rules or business logic. The LLM's reasoning ability enables it to create autonomous workflows on the fly."
        }
      ].map((item, index) => (
        <li key={index} className="p-4 bg-gray-50 rounded-md shadow-sm">
          <h3 className="text-xl font-semibold text-gray-700 mb-2">{item.title}</h3>
          <p className="text-gray-600 leading-relaxed">{item.text}</p>
        </li>
      ))}
    </ul>
    <p className="text-lg text-gray-700 leading-relaxed">
      Even though the functionality here is limited to drawing and shuffling cards, this is a powerful demonstration of how LLM-based agents can act as a universal interface layer for any backend service with reasonable API endpoints. With minimal glue code, LLMs can bridge the gap between natural language and programmatic APIs, opening up new possibilities for rapid prototyping, automation, and conversational interfaces.
    </p>
  </section>
);

const SpecialThanksSection = () => (
  <blockquote className="mt-8 mb-6 p-6 border-l-4 border-green-500 bg-green-50 rounded-md shadow">
    <p className="text-gray-700 leading-relaxed">
      <strong>Special thanks again to{' '}
      <a
        href="https://deckofcardsapi.com/"
        target="_blank"
        rel="noopener noreferrer"
        className="text-green-600 hover:text-green-800 font-medium underline"
      >
        Chase Roberts
      </a>{' '}
      for providing the Deck of Cards API, which made this demonstration possible. The open and well-documented API was essential in showcasing how LLM agents can interact with real-world services with minimal effort.</strong>
    </p>
  </blockquote>
);

function LandingPage() {
  return (
    <div className="p-4 md:p-8 max-w-4xl mx-auto bg-white rounded-xl shadow-2xl space-y-8">
      <header className="text-center py-6">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-800">
          Demo ADK App
        </h1>
        <p className="text-lg text-gray-600 mt-2">
          Exploring Google's ADK and the Power of LLMs
        </p>
      </header>
      <AcknowledgementSection />
      <IntroductionSection />
      <PowerOfLLMsSection />
      <SpecialThanksSection />
    </div>
  );
}

export default LandingPage;
