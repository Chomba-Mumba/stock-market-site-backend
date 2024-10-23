import react from 'react';
import { Navbar } from '../../components/Navbar/Navbar';
import { StockData } from './StockData';
import { ModelConsensus } from './ModelConsensus';
import { QuantitativeAnalysis } from './QuantitativeAnalysis';
import { StockGraph } from './StockGraph';
import { StockReportHeader } from './StockReportHeader';

import './Home.module.css';

export function Home() {
  return (
    <div className="Home">
      <header className="Home-header">
        <Navbar />
        <div className="Home-header-content">
          <h1>FTSE 100 Stock Market Prediction</h1>
        </div>
      </header>
      <body>
        <div className='Home-Container'>
            <div className='Stock-Report-Header'>
              <StockReportHeader/>
            </div>
            <div className='Stock-Data-Div'>
                <StockData/>
            </div>
            <div className='Stock-Graph-Div'>
                <StockGraph/>
            </div>
            <div className='Model-Consensus-Div'>
                <ModelConsensus/>
            </div>
            <div className='Quantitative-Analysis-Div'>
                <QuantitativeAnalysis/>
            </div>
        </div>
        
      </body>
    </div>
  );
}