import React, { useState } from 'react';
import './App.css';
import ChatBot from './components/ChatBot';
import { ReactComponent as ChatIcon } from './chat-icon.svg'; // Assuming you have an SVG icon
import Sidebar from './components/SideBar';
import Cards from './components/Cards';
<ChatIcon className="chat-icon" />
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRocketchat } from '@fortawesome/free-brands-svg-icons';// Using the comment icon as an example

function App() {
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [isChatVisible, setIsChatVisible] = useState(false);

  // Function to toggle sidebar visibility
  // const toggleSidebar = () => {
  //   setIsSidebarVisible(!isSidebarVisible);
  // };

  return (
    <div className={`App ${isChatVisible ? 'chat-active' : ''}`}>
      <header>Dashboard</header>
      <Sidebar isOpen={isSidebarVisible} toggleSidebar={() => setIsSidebarVisible(!isSidebarVisible)} />
      <div className={`main-content ${isSidebarVisible ? 'sidebar-visible' : 'sidebar-closed'}`}>
        <Cards />
      </div>
      <div className="chat-toggle" onClick={() => setIsChatVisible(!isChatVisible)}>
        <FontAwesomeIcon icon={faRocketchat} className={`chat-icon ${isChatVisible ? 'active' : ''}`} size="3x" />
      </div>
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
