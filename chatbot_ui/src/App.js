import React, { useState } from 'react';
import './App.css';
import ChatBot from './components/ChatBot';
import { ReactComponent as ChatIcon } from './chat-icon.svg'; // Assuming you have an SVG icon

function App() {
  const [isChatVisible, setIsChatVisible] = useState(false);

  return (
    <div className="App">
      <header>Header Content</header>
      <aside className={isChatVisible ? 'dashboard visible' : 'dashboard'}>Dashboard Content</aside>
      <footer>Footer Content</footer>
      <div className="chat-toggle" onClick={() => setIsChatVisible(!isChatVisible)}>
        <ChatIcon />
      </div>
      {isChatVisible && <ChatBot />}
    </div>
  );
}

export default App;
