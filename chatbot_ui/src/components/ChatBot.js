// import React, { useState } from 'react';
// import './ChatBot.css';

// const ChatBot = () => {
//   const [messages, setMessages] = useState([]);
//   const [inputText, setInputText] = useState('');
//   const [attachedFile, setAttachedFile] = useState(null);

//   const sendMessage = async () => {
//     if (!inputText.trim() && !attachedFile) return;

//     // Add the user's message to the chat
//     const userMessage = { text: inputText, sender: 'user' };
//     setMessages(messages => [...messages, userMessage]);

//     const formData = new FormData();
//     formData.append('question', inputText);
//     if (attachedFile) {
//       formData.append('file', attachedFile);
//     }

//     const response = await fetch(`http://localhost:8000/ask-pdf`, {
//       method: 'POST',
//       // No 'Content-Type' header required; browser will set it to 'multipart/form-data'
//       body: formData,
//     });

//     if (response.ok) {
//       const data = await response.json();
//       setMessages(messages => [...messages, { text: data.answer, sender: 'bot' }]);
//     } else {
//       // Handle error...
//       setMessages(messages => [...messages, { text: "Failed to get a response from the server.", sender: 'bot' }]);
//     }

//     setInputText('');
//     setAttachedFile(null); // Clear the attached file after sending
//   };

//   return (
//     <div className="chat-container">
//       <div className="chat-header">Doc Chat Bot</div>
//       <div className="chat-messages">
//         {messages.map((message, index) => (
//           <div key={index} className={`message ${message.sender}`}>
//             {message.text}
//           </div>
//         ))}
//       </div>
//       <div className="chat-input">
//         <input
//           type="text"
//           value={inputText}
//           onChange={(e) => setInputText(e.target.value)}
//           onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
//           placeholder="Type your message here..."
//         />
//         <input
//           type="file"
//           onChange={(e) => setAttachedFile(e.target.files[0])} // Taking the first file
//         />
//         <button onClick={sendMessage}>Send</button>
//       </div>
//     </div>
//   );
// };

// export default ChatBot;




import React, { useState } from 'react';
import './ChatBot.css';

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [attachedFile, setAttachedFile] = useState(null);

  const sendMessage = async () => {
    // Add the user's message or file upload status to the chat
    let userMessage = { text: inputText, sender: 'user' };
    if (attachedFile) {
      userMessage = { ...userMessage, text: `Uploading file: ${attachedFile.name}` };
    }
    setMessages(messages => [...messages, userMessage]);

    if (attachedFile) {
      // If there's an attached file, upload it
      const formData = new FormData();
      formData.append('file', attachedFile);

      const uploadResponse = await fetch(`http://localhost:8000/upload-pdf`, {
        method: 'POST',
        body: formData,
      });

      if (uploadResponse.ok) {
        // After uploading, you might want to send a follow-up question to the 'ask-pdf' endpoint
        // or handle the uploaded file response as needed.
        const uploadData = await uploadResponse.json();
        setMessages(messages => [...messages, { text: `Here are your job matches ${uploadData.data}`, sender: 'bot' }]);
      } else {
        setMessages(messages => [...messages, { text: "Failed to upload the file.", sender: 'bot' }]);
      }
    } else if (inputText.trim()) {
      // If there's text input but no file, send it to the 'ask-pdf' endpoint
      const formData = new FormData();
      formData.append('question', inputText);

      const response = await fetch(`http://localhost:8000/ask-pdf`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(messages => [...messages, { text: data.answer, sender: 'bot' }]);
      } else {
        setMessages(messages => [...messages, { text: "Failed to get a response from the server.", sender: 'bot' }]);
      }
    }

    // Reset input and file after sending
    setInputText('');
    setAttachedFile(null);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">Doc Chat Bot</div>
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message here..."
        />
        <input
          type="file"
          onChange={(e) => setAttachedFile(e.target.files[0])}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatBot;
