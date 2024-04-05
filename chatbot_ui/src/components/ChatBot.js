// ChatBot.js
import React, { useState, useEffect } from 'react';
import './ChatBot.css';
import { Button, TextField, Paper, Typography, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel } from '@mui/material'; // Import Fade for animation
import { Box} from '@mui/material';

const OptionButtons = ({ onSelectOption }) => (
  <FormControl component="fieldset">
    <FormLabel component="legend">Choose an option</FormLabel>
    <RadioGroup aria-label="chat-options">
      <Box sx={{ '& .MuiFormControlLabel-root': { mb: 2 } }}> {/* Apply bottom margin to each FormControlLabel */}
        <FormControlLabel value="1" control={<Radio />} label="Homework Helper" onClick={() => onSelectOption('1')} />
        <FormControlLabel value="2" control={<Radio />} label="Job Matching" onClick={() => onSelectOption('2')} />
        <FormControlLabel value="3" control={<Radio />} label="Exam Prep Aid" onClick={() => onSelectOption('3')} />
      </Box>
    </RadioGroup>
  </FormControl>
);

const ChatBot = () => {
  const [messages, setMessages] = useState([{ text: 'Select an option:\n1) Homework Helper \n2) Job Matching \n3) Exam Prep Aid', sender: 'bot' }]);
  const [inputText, setInputText] = useState('');
  const [attachedFile, setAttachedFile] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  const [mcqs, setMcqs] = useState([]);
  const [selections, setSelections] = useState({});


  useEffect(() => {
    // Initialize the chat with the option buttons message
    const initialMessage = {
      text: 'Select an option:\n1) Homework Helper\n2) Job Matching\n3) Exam Prep Aid',
      sender: 'bot',
      withOptions: true, // custom property to indicate this message has options
    };
    setMessages([initialMessage]);
  }, []);

  const handleOptionSelection = async (option) => {
    setSelectedOption(option);
    let formData = new FormData();
    // Fetch the MCQs for exam prep when that option is selected
    if (option === '3') {
      formData.append('question', "inputText");
      // const response = await fetch('http://localhost:8000/exam-prep-aid-generation/', {
      //   method: 'POST',
      //   body: formData
      // });
      const response = await fetch('http://localhost:8000/exam-prep-aid-generation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: "inputText" }), // Make sure inputText is the format expected by the server
      });
      if (response.ok) {
        const data = await response.json();
        setMcqs(data.mcqs);
        setSelections({}); // Reset selections when new MCQs are fetched
      } else {
        // Handle errors
        console.error('Failed to fetch MCQs');
      }
    }
  };

  const handleMCQSelection = (mcqId, option) => {
    setSelections(prev => ({ ...prev, [mcqId]: option }));
  };



  const submitAnswers = async () => {
    
    const response = await fetch('http://localhost:8000/exam-prep-aid-evaluation', {
      method: 'POST',
      body: JSON.stringify({ selections, mcqs }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (response.ok) {
      const result = await response.json();
      // Display result to user
      console.log(result);
      setMcqs(result);
      setSelections({});
    } else {
      // Handle errors
      console.error('Failed to submit answers');
    }
  };

  const sendMessage = async () => {
    if (!inputText.trim() && !attachedFile) return;
    let apiEndpoint = '';
    let formData = new FormData();

    if (selectedOption === '1') {
      apiEndpoint = 'ask-pdf';
      formData.append('question', inputText);
    } else if (selectedOption === '2' && attachedFile) {
      apiEndpoint = 'upload-pdf';
      formData.append('file', attachedFile);
    } else if (selectedOption === '3') {
      // apiEndpoint = 'exam-prep-aid-generation';
      // formData.append('question', inputText);
    } else {
      setMessages(messages => [...messages, { text: "Please select an option and provide the necessary input.", sender: 'bot' }]);
      return;
    }

    const userMessage = { text: inputText, sender: 'user' };
    setMessages(messages => [...messages, userMessage]);

    const response = await fetch(`http://localhost:8000/${apiEndpoint}`, {
      method: 'POST',
      body: formData,
    });

    if (selectedOption === '1') {

      if (response.ok) {
        const data = await response.json();
        setMessages(messages => [...messages, { text: data.answer, sender: 'bot' }]);
      } else {
        setMessages(messages => [...messages, { text: "Failed to get a response from the server.", sender: 'bot' }]);
      }
    } else if (selectedOption === '2' && attachedFile) {
      if (response.ok) {
        const data = await response.json();
        setMessages(messages => [...messages, { text: `Here are your job matches ${data.data}`, sender: 'bot' }]);
      } else {
        setMessages(messages => [...messages, { text: "Failed to upload the file.", sender: 'bot' }]);
      }
    } 
 

    setInputText('');
    setAttachedFile(null);
  };

//   return (
//     <div className="chat-container">
//       <div className="chat-header">Doc Chat Bot</div>
//       <div className="chat-messages">
//         {messages.map((message, index) => (
//           <div key={index} className={`message ${message.sender}`}>
//             {message.text}
//           </div>
//         ))}
//         {selectedOption === '3' && mcqs.map(mcq => (
//           <div key={mcq.id} className="mcq-container">
//             <p>{mcq.wholeQuestion}</p>
//             {mcq.allOptions.map(option => (
//               <label key={option}>
//                 <input
//                   type="radio"
//                   name={`mcq-${mcq.id}`}
//                   value={option}
//                   checked={selections[mcq.id] === option}
//                   onChange={() => handleMCQSelection(mcq.id, option)}
//                 />
//                 {option}
//               </label>
//             ))}
//           </div>
//         ))}
//         {selectedOption === '3' && (
//           <button className="submit-mcqs-btn" onClick={submitAnswers}>
//             Submit Answers
//           </button>
//         )}
//       </div>
//       {selectedOption ? (
//         <div className="chat-input">
//           <input
//             type="text"
//             value={inputText}
//             onChange={(e) => setInputText(e.target.value)}
//             onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
//             placeholder={selectedOption === '1' ? "Ask your question..." : "Input for exam prep..."}
//           />
//           {selectedOption === '2' && (
//             <input
//               type="file"
//               onChange={(e) => setAttachedFile(e.target.files[0])}
//             />
//           )}
//           <button onClick={sendMessage}>Send</button>
//         </div>
//       ) : (
//         <div className="options-input">
//           <button onClick={() => handleOptionSelection('1')}>Homework Helper</button>
//           <button onClick={() => handleOptionSelection('2')}>Job Matching</button>
//           <button onClick={() => handleOptionSelection('3')}>Exam Prep Aid</button>
//         </div>
//       )}
//     </div>
//   );
// };

return (
  // Changes start from line 50
  <Paper elevation={3} className="chat-container">
    <Typography variant="h6" className="chat-header">VATS-AI Buddy</Typography>
    <div className="chat-messages">
      {messages.map((message, index) => (
        <Typography key={index} component="div" className={`message ${message.sender}`}>
          {message.text}
          {message.withOptions && <OptionButtons onSelectOption={handleOptionSelection} />}
        </Typography>
      ))}
      {selectedOption === '3' && mcqs.map(mcq => (
        <Paper key={mcq.id} className="mcq-container">
          <Typography variant="body1">{mcq.wholeQuestion}</Typography>
          <RadioGroup name={`mcq-${mcq.id}`} value={selections[mcq.id] || ''} onChange={(event) => handleMCQSelection(mcq.id, event.target.value)}>
            {mcq.allOptions.map(option => (
              <FormControlLabel key={option} value={option} control={<Radio />} label={option} />
            ))}
          </RadioGroup>
        </Paper>
      ))}
      {selectedOption === '3' && (
        <Button variant="contained" color="primary" onClick={submitAnswers} className="submit-mcqs-btn">Submit Answers</Button>
      )}
    </div>
    {selectedOption ? (
      <div className="chat-input">
        <TextField fullWidth label="Type your message here..." variant="outlined" value={inputText} onChange={(e) => setInputText(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} />
        {selectedOption === '2' && (
          // Assuming you'll adjust file input styling accordingly
          <input type="file" onChange={(e) => setAttachedFile(e.target.files[0])} style={{margin: '0 10px'}} />
        )}
        <Button variant="contained" color="primary" onClick={sendMessage}>Send</Button>
      </div>
    ) : null}
  </Paper>
  // Changes end at line 83
);
};

export default ChatBot; 