// frontend-new/src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import Comments from './components/comments';

// Pass a valid taskId here
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    
    <Comments taskId={1} />
  </React.StrictMode>
);

reportWebVitals();
