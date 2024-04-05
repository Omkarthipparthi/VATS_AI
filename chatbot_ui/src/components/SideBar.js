import React from 'react';
import { IconButton, List, ListItemIcon, ListItemText } from '@mui/material';

import AccountBoxIcon from '@mui/icons-material/AccountBox';
import DashboardIcon from '@mui/icons-material/Dashboard';
import BookIcon from '@mui/icons-material/Book';
import GroupIcon from '@mui/icons-material/Group';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import InboxIcon from '@mui/icons-material/Inbox';
import HistoryIcon from '@mui/icons-material/History';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
// import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import './Sidebar.css'; // This will be your CSS file for Sidebar styling

const Sidebar = ({isOpen, toggleSidebar}) => {
  return (
    <div className={`sidebar ${isOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
    <IconButton onClick={toggleSidebar} className="toggle-button">
    {isOpen ? <ChevronLeftIcon /> : <ChevronRightIcon />}
    </IconButton>
    <List component="nav" className={`sidebar-content ${!isOpen && 'content-closed'}`}>
          <ListItemIcon>
            <AccountBoxIcon />
          </ListItemIcon>
          <ListItemText primary="Account" />
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        <ListItemIcon>
            <BookIcon />
        </ListItemIcon>
          <ListItemText primary="Book" />
        <ListItemIcon>
            <GroupIcon />
          </ListItemIcon>
          <ListItemText primary="Group" />
          <ListItemIcon>
            <CalendarTodayIcon />
          </ListItemIcon>
          <ListItemText primary="Calendar" />
          <ListItemIcon>
            <InboxIcon />
          </ListItemIcon>
          <ListItemText primary="Inbox" />
          <ListItemIcon>
            <HistoryIcon />
          </ListItemIcon>
          <ListItemText primary="History" />
          <ListItemIcon>
            <HelpOutlineIcon />
          </ListItemIcon>
          <ListItemText primary="Help" />
      </List>
    </div>
  );
};

export default Sidebar;
