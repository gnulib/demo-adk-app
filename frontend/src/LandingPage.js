import React from 'react';

function LandingPage() {
  return (
    <div className="p-6 max-w-2xl mx-auto">
      <blockquote className="mb-4 p-4 border-l-4 border-gray-300 bg-gray-100">
        <p className="text-lg font-semibold mb-2">Acknowledgement:</p>
        <p className="text-base">
          This project makes use of the excellent{' '}
          <a
            href="https://deckofcardsapi.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-700 underline"
          >
            Deck of Cards API
          </a>{' '}
          by Chase Roberts. Many thanks to Chase for providing this fun and useful API!
        </p>
      </blockquote>

      <p className="text-xl mb-4">
        This is a demo project for a simple app using{' '}
        <a
          href="https://google.github.io/adk-docs/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 hover:text-blue-700 underline"
        >
          Google's ADK
        </a>{' '}
        framework. This project is intended to demonstrate how to setup a GCP project for deploying ADK app as a cloud run service.
      </p>
      <p className="text-xl mb-4">
        Secondary objective of this project is to demonstrate the power of LLMs, how they can be used to build conversation interface against pretty much any service that has reasonable APIs.
      </p>

      <h2 className="text-2xl font-bold mt-6 mb-3">The Power of LLM-based Agents as Middleware</h2>
      <p className="text-xl mb-4">
        This project, while simple in functionality, demonstrates the remarkable power of Large Language Models (LLMs) as middleware for backend services. The agent in this demo is able to:
      </p>
      <ul className="list-disc list-inside mb-4 pl-4 text-xl">
        <li className="mb-2">
          <strong>Understand API Capabilities from Docstrings:</strong> The agent uses the docstrings of simple Python wrapper functions to understand what each API call does. No additional schema, OpenAPI spec, or manual translation is required—just clear function docstrings.
        </li>
        <li className="mb-2">
          <strong>Interpret API Responses Directly:</strong> The agent can read and reason about the raw API responses (typically JSON), extracting the information it needs without any custom parsing or mapping logic.
        </li>
        <li className="mb-2">
          <strong>Autonomously Orchestrate Workflows:</strong> Given a user request, the agent can decide which API(s) to call, in what order, and how to use the results—without any hardcoded rules or business logic. The LLM's reasoning ability enables it to create autonomous workflows on the fly.
        </li>
      </ul>
      <p className="text-xl mb-4">
        Even though the functionality here is limited to drawing and shuffling cards, this is a powerful demonstration of how LLM-based agents can act as a universal interface layer for any backend service with reasonable API endpoints. With minimal glue code, LLMs can bridge the gap between natural language and programmatic APIs, opening up new possibilities for rapid prototyping, automation, and conversational interfaces.
      </p>
      <blockquote className="mt-6 mb-4 p-4 border-l-4 border-gray-300 bg-gray-100">
        <p className="text-base">
          <strong>Special thanks again to{' '}
          <a
            href="https://deckofcardsapi.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-700 underline"
          >
            Chase Roberts
          </a>{' '}
          for providing the Deck of Cards API, which made this demonstration possible. The open and well-documented API was essential in showcasing how LLM agents can interact with real-world services with minimal effort.</strong>
        </p>
      </blockquote>
    </div>
  );
}

export default LandingPage;
