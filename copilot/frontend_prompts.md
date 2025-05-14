
#### prompt - add login and logout buttons to the app ####

Modify the app to add login and logout, using the firebase userLogin and userLogout methods as following
- modify landing page to show a login form inline with rest of the content
- keep app title on top, then login form, followed by brief description of the project, acknowledgement etc
- when user is logged in, landpage should not be displayed and instead actual app functionality should be displayed
- app functionality will be described later, for now just show a placeholder simple canvas, with user's details from authenticated user info from userLogin
- when user logs out, then show the landing page again

#### prompt - create landing page for the app ####

Implement the landing page for react frontend as following:
  - provide a summary of the project, using contents from https://raw.githubusercontent.com/gnulib/demo-adk-app/refs/tags/blog-part-1/README.md to describe purpose of the project
  - The LandingPage component should display an overview of the project using the provided README content Specifically, include:
    - The Acknowledgement section.
    - The main introductory paragraph starting with "This is a demo project...".
    - The section titled "The Power of LLM-based Agents as Middleware".
    - You can ignore the setup and "Getting Started" sections for the landing page display.
    - Format the text using appropriate HTML tags (like <h2>, <p>, <blockquote>, <strong>) and apply some basic Tailwind classes for readability (e.g., text-xl, mb-4, p-6, max-w-2xl, mx-auto).
    - The App component should initially render the LandingPage component.
    - Ensure the HTML structure includes the necessary <script> tags for React, ReactDOM, Babel, and the Tailwind CSS CDN link within the <head> or <body>.
- keep the content on landing page brief and succint, with link to the github README for more details.

#### prompt - add firebase methods for password authentication ####

create a utility for firebase authentication in the react project as following:
- import getAuth, signInWithEmailAndPassword and signOut from "firebase/auth"
- initialize "auth" using getAuth method
- implement a login method, that uses signInWithEmailAndPassword as following and returns back authenticated user credenial, or error:
```
signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Signed in 
    const user = userCredential.user;
    // ...
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
  });
  ```
- implement a logout method, that uses signOut as following and returns back success or error:
```
signOut(auth).then(() => {
  // Sign-out successful.
}).catch((error) => {
  // An error happened.
});
```
- implement the methods using modern async/await pattern


#### prompt - create a firebase app for use in frontend ####

create a component or utility for initializing firebase app in react project under frontend as following:
- uses import { initializeApp } from 'firebase/app';
- initializes a json object with following schema, and populates the values from environment variables in placeholder values:
```
{
  projectId: "REACT_APP_FIREBASE_PROJECT_ID",
  appId: "REACT_APP_FIREBASE_APP_ID",
  storageBucket: "REACT_APP_FIREBASE_STORAGE_BUCKET",
  apiKey: "REACT_APP_FIREBASE_API_KEY",
  authDomain: "REACT_APP_FIREBASE_AUTH_DOMAIN",
  messagingSenderId: "REACT_APP_FIREBASE_MESSAGING_SENDER_ID"
}
```
- initializes app using above json object and configuration
- exports that app to be used in other utility methods for firebase functionality
