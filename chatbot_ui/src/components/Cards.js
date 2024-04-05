import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import './Cards.css'; // This will be your CSS file for Cards styling

const CardData = [
  // Array of objects representing each card's data
  {
    title: 'CSE 535: Mobile Computing',
    semester: '2023 Fall',
    color: '#1e4620',
  },
  {
    title: 'CSE 573: Semantic Web Mining',
    semester: '2023 Fall',
    color: '#E97451',
  },
  {
    title: 'CSE 545: Software Security',
    semester: '2024 Fall',
    color: '#702963',
  },
];

const CourseCard = ({ title, code, semester, color }) => {
  return (
    <Card className="course-card" style={{ backgroundColor: color }}>
      <CardContent>
        <Typography variant="h5" component="h2">
          {title}
        </Typography>
        <Typography color="textSecondary">
          {code}
        </Typography>
        <Typography variant="body2" component="p">
          {semester}
        </Typography>
      </CardContent>
    </Card>
  );
};

const Cards = () => {
  return (
    <div className="cards-container">
      {CardData.map((card, index) => (
        <CourseCard key={index} {...card} />
      ))}
    </div>
  );
};

export default Cards;
