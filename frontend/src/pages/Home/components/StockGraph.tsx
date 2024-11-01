import React from 'react';
import './StockGraph.modules.css';

import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
//TODO - add changing data to the graph, Current stats, model predictions, previous years data. use filter
const data = [
  {
    name: '01/11/2024', 
    open: 150, 
    close: 151, 
    high: 132, 
    low: 134
  }, 
  {
    name: '31/10/2024', 
    open: 234, 
    close: 151, 
    high: 132, 
    low: 134
  }, 
  {
    name: '30/10/2024', 
    open: 200, 
    close: 151, 
    high: 132, 
    low: 134
  }, 
  {
      name: '29/10/2024', 
      open: 160, 
      close: 151, 
      high: 132, 
      low: 134
  }
];

const renderLineChart = (
  <LineChart width={1000} height={400} data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
    <Line type="monotone" dataKey="open" stroke="#8884d8" />
    <Line type="monotone" dataKey="close" stroke="#82ca9d" />
    {/* // TODO make high low values optional */}
    <Line type="monotone" dataKey="high" stroke="#FF0000" />
    <Line type="monotone" dataKey="low" stroke="#FFFF00" />
    <CartesianGrid stroke="#ccc" />
    <XAxis dataKey="name" />
    <YAxis />
    <Tooltip />
  </LineChart>
);

export function StockGraph() {
  return (
    <div className="stock-graph">
      {renderLineChart}
    </div>
  );
}
