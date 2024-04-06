import React from 'react';
import { Card, CardActionArea, CardContent, Typography } from '@mui/material';
import './Cards.css'; // Make sure your CSS file path is correct

const CardData = [
  {
    title: 'CSE 101: Fundamentals of Statistics',
    semester: '2023 Fall',
    color: '#6d597a',
  },
  {
    title: 'CSE 573: Semantic Web Mining',
    semester: '2023 Spring',
    color: '#b56576',
  },
  // {
  //   title: 'CSE 545: Software Security',
  //   semester: '2024 Fall',
  //   color: '#b7b7a4',
  // },
  // {
  //   title: 'CSE 578: Data Visualization',
  //   semester: '2024 Spring',
  //   color: '#223843',
  // },
];

const CourseCard = ({ title, semester, color }) => {
  return (
    <Card className="course-card" style={{ backgroundColor: color }}>
      <CardActionArea>
        <CardContent>
          <Typography gutterBottom variant="h5" component="h2" style={{ color: '#fff' }}>
            {title}
          </Typography>
          <Typography variant="body2" component="p" style={{ color: '#f5f5f5' }}>
            {semester}
          </Typography>
        </CardContent>
      </CardActionArea>
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