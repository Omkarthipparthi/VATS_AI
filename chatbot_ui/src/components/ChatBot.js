// ChatBot.js
import React, { useState, useEffect } from 'react';
import './ChatBot.css';
import { Button, TextField, Paper, Typography, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel } from '@mui/material'; // Import Fade for animation
import { Box} from '@mui/material';


const correctStyle = {
  backgroundColor: 'green',
  color: 'white',
};
const incorrectStyle = {
  backgroundColor: 'red',
  color: 'white',
};

const OptionButtons = ({ onSelectOption, options }) => {
  const optionLabels = {
    '1': 'Homework Helper',
    '2': 'Job Matching',
    '3': 'Exam Prep Aid',
    '4': 'More Questions',
    '5': 'EXIT'
    // ... Add more if you have other options
  };
  
  const safeOptions = Array.isArray(options) ? options : [];
  return (
    <FormControl component="fieldset">
      <FormLabel component="legend">Choose an option</FormLabel>
      <RadioGroup aria-label="chat-options">
        <Box sx={{ '& .MuiFormControlLabel-root': { mb: 2 } }}>
          {safeOptions.map(option => (
            <FormControlLabel
              key={option}
              value={option}
              control={<Radio />}
              label={optionLabels[option]}
              onClick={() => onSelectOption(option)}
            />
          ))}
        </Box>
      </RadioGroup>
    </FormControl>
  );
};



const ChatBot = () => {
  const [messages, setMessages] = useState([{ text: 'Select an option:\n1) Homework Helper \n2) Job Matching \n3) Exam Prep Aid', sender: 'bot' }]);
  const [inputText, setInputText] = useState('');
  const [attachedFile, setAttachedFile] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  const [mcqs, setMcqs] = useState([]);
  const [selections, setSelections] = useState({});
  const [fileName, setFileName] = useState('')

  useEffect(() => {
    const initialMessage = {
      text: 'Select an option:\n1) Homework Helper\n2) Job Matching\n3) Exam Prep Aid',
      sender: 'bot',
      withOptions: true,
      options: ['1', '2', '3'] // Corresponding to Homework Helper, Job Matching, Exam Prep Aid
    };
    setMessages([initialMessage]);
    console.log("Initial messages:", messages);
  }, []);
  
  const handleEvaluationResults = (results) => {
    const updatedMcqs = mcqs.map(mcq => {
      const result = results.find(r => r.id === mcq.id);
      return {
        ...mcq,
        isCorrect: result ? result.isCorrect : undefined,
        userSelected: result ? result.userSelected : undefined,
      };
    });
    setMcqs(updatedMcqs);
  };


  // Add a function to handle file selection, after line 40


  const FilesManager = (event) =>{
    setAttachedFile(event.target.files[0]); 
    handleFileChange(event);
  }

  const handleFileChange = (event) => {

    const file = event.target.files[0];

    if (file) {

      setAttachedFile(file);

      setFileName(file.name); // Update the filename state

      setMessages(messages => [...messages, { text: `File selected: ${file.name}`, sender: 'user' }]);

    }

  };
  const handleOptionSelection = async (option) => {
    console.log(`Option selected: ${option}`);
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

  // const handleMCQSelection = (mcqId, option) => {
  //   setSelections(prevSelections => ({
  //     ...prevSelections,
  //     [mcqId]: option
  //   }));
  // };

  const handleMCQSelection = (mcqId, option) => {
    setMcqs(mcqs.map(mcq => {
      if (mcq.id === mcqId) {
        // Here you evaluate the option right away and set the isCorrect property
        return {
          ...mcq,
          userSelected: option,
          isCorrect: mcq.correctOption === option
        };
      }
      return mcq;
    }));
    setSelections(prevSelections => ({
      ...prevSelections,
      [mcqId]: option
    }));
  };
  

  const formatJobMatches = (text) => {
    return text.split('\n').map((line, index, array) => (
      <React.Fragment key={index}>
        {line}{index !== array.length - 1 && <br />}
      </React.Fragment>
    ));
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
      setMessages(messages => [...messages, { text: `Uploading file: ${fileName}`, sender: 'user' }]); // Display the uploading file message

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
        // setMessages(messages => [...messages, { text: `Here are your job matches ${data.data}`, sender: 'bot' }]);
        const formattedText = formatJobMatches(data.data);
        setMessages(messages => [...messages, { text: <>{'Here are your job matches'}{formattedText}</>, sender: 'bot' }]);
      
      
      } else {
        setMessages(messages => [...messages, { text: "Failed to upload the file.", sender: 'bot' }]);
      }
    } 
 

    setInputText('');
    setAttachedFile(null);
  };

return (
  // Changes start from line 50
  <Paper elevation={3} className="chat-container">
    <Typography variant="h6" className="chat-header">VATS-AI Buddy</Typography>
    <div className="chat-messages">
    {messages.map((message, index) => {
      // Log the message to the console for debugging purposes
      console.log(`Rendering message:`, message);

      
      return (
        <div key={index} className={`message ${message.sender}`}>
          <Typography>{message.text}</Typography>
          {message.withOptions && (
            <OptionButtons
              onSelectOption={handleOptionSelection}
              options={ message.options}
            />
          )}
        </div>
      );
    })}

{selectedOption === '3' && mcqs.map(mcq => (
  <Paper key={mcq.id} className="mcq-container">
    <Typography variant="body1">{mcq.wholeQuestion}</Typography>
    <RadioGroup name={`mcq-${mcq.id}`} value={selections[mcq.id] || ''}
    onChange={(event) => handleMCQSelection(mcq.id, event.target.value)}>
      {mcq.allOptions.map(option => {
        // Determine the style based on whether the option is correct, incorrect,
        // and whether it should be highlighted as the correct answer
        const isUserSelected = selections[mcq.id] === option;
        let optionStyle = {};
        if (isUserSelected) {
          optionStyle = mcq.isCorrect ? correctStyle : incorrectStyle;
        } else if (!isUserSelected && mcq.correctOption === option && selections[mcq.id] !== undefined) {
          // Apply correctStyle to the correct option if a wrong option was selected
          optionStyle = correctStyle;
        }
        return (
          <FormControlLabel
            key={option}
            value={option}
            control={<Radio />}
            label={option}
            style={optionStyle}
          />
        );
      })}
    </RadioGroup>
  </Paper>
))}


      {selectedOption === '3' && (
        <Button variant="contained" color="primary" onClick={submitAnswers} className="submit-mcqs-btn">Submit Answers</Button>
      )}
    </div>
    {selectedOption ? (
      <div className="chat-input">
        <TextField fullWidth label="Type your message here..." variant="outlined" value={inputText} 
        onChange={(e) => setInputText(e.target.value)} 
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()} />
        {selectedOption === '2' && (
          // Assuming you'll adjust file input styling accordingly
          <input type="file" onChange={FilesManager} style={{margin: '0 10px'}} 
          />
        )}
        <Button variant="contained" color="primary" onClick={sendMessage}>Send</Button>
      </div>
    ) : null}
  </Paper>
  // Changes end at line 83
);
};

export default ChatBot; 