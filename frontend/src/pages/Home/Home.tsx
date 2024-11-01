import react from 'react';
import { Navbar } from '../../components/Navbar/Navbar';
import { StockData } from './components/StockData';
import { ModelConsensus } from './components/ModelConsensus';
import { StockGraph } from './components/StockGraph';
import { StockReportHeader } from './components/StockReportHeader';
import { MarketPanel } from './components/MarketPanel';

import './Home.module.css';
// TODO - make website dark theme?
export function Home() {
  return (
    <div className="Home">
      <header className="Home-header">
        <Navbar />
      </header>
      <body>
        <div className='Home-Container'>
            <div className='Market-Panel'>
              <MarketPanel/>
            </div>
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
        </div>
        
      </body>
    </div>
  );
}