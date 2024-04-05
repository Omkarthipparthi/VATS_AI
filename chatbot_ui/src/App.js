import React, { useState } from 'react';
import './App.css';
import ChatBot from './components/ChatBot';
import { ReactComponent as ChatIcon } from './chat-icon.svg'; // Assuming you have an SVG icon
import Sidebar from './components/SideBar';
import Cards from './components/Cards';
<ChatIcon className="chat-icon" />

function App() {
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [isChatVisible, setIsChatVisible] = useState(false);

  // Function to toggle sidebar visibility
  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible);
  };

  return (
    <div className={`App ${isChatVisible ? 'chat-active' : ''}`}>
      <header>Dashboard</header>
      <Sidebar isOpen={isSidebarVisible} toggleSidebar={toggleSidebar} />
      <div className={`main-content ${isSidebarVisible ? 'sidebar-visible' : 'sidebar-closed'}`}>
        <Cards />
      </div>
      <footer>ASU</footer>
      <div className="chat-toggle" onClick={() => setIsChatVisible(!isChatVisible)}>
      <div className="chat-icon">
        <ChatIcon />
      </div></div>
      {isChatVisible && (
        <>
          <div className="chat-overlay"></div>
          <ChatBot />
        </>
      )}
    </div>
  );
}

export default App;
