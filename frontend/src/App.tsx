import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import {Home} from './pages/Home/Home';

export const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* 
        // <Route path="/stock-data" element={<StockData />} />

 
        // <Route path="/graph" element={<Graph />} /> */}

      </Routes>
    </Router>
  );
};

