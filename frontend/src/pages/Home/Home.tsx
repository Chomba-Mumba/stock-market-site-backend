import react from 'react';
import { Navbar } from '../../components/Navbar/Navbar';
import { StockData } from './components/StockData';
import { ModelConsensus } from './components/ModelConsensus';
import { StockGraph } from './components/StockGraph';
import { StockReportHeader } from './components/StockReportHeader';
import { MarketPanel } from './components/MarketPanel';
import styles from './Home.module.css';

import './Home.module.css';
// TODO - make website dark theme?
const stockNews = [
  {
    title: "What the Sigma?",
    content: "Sigma Corporation has been making waves in the stock market recently. The company has been making a lot of acquisitions and has been expanding its product line. The company's stock has been on the rise and many analysts are predicting that it will continue to grow in the coming months.",
    date: "01/11/2024",
    source: "Bloomberg",
    thumbnail: "photo1.jpg"
  },
  {
    title: "Green Fn Slide",
    content: "Green Fn has been struggling in the stock market recently. The company has been facing a lot of competition and has been losing market share. The company's stock has been on the decline and many analysts are predicting that it will continue to fall in the coming months.",
    date: "01/11/2024",
    source: "Bloomberg",
    thumbnail: "pokemon-confused.gif"
  },
  {
    title: "Brainrot", 
    content: "Noah is Fat",
    date: "01/11/2024",
    source: "Bloomberg",
    thumbnail: "logo.jpg"
  },
  {
    title: "text", 
    content: "Noah is Fat",
    date: "01/11/2024",
    source: "Bloomberg",
    thumbnail: "logo.jpg"
  }
]
export function Home() {
  return (
    <div className={styles.Home}>
      <header className={styles['Home-header']}>
        <Navbar />
      </header>
      <main className={styles['Home-Container']}>
        <div className={styles['Market-Panel']}>
          <MarketPanel />
        </div>
        
        <div className={styles['Stock-Report-Header']}>
          <StockReportHeader />
        </div>
        
        <div className={styles['Home-Container-Data']}>
          <div className={styles['Stock-Data-Div']}>
            <StockData />
          </div>
          
          <div className={styles['Stock-Graph-Div']}>
            <StockGraph />
          </div>
          
          <div className={styles['Model-Consensus-Div']}>
            <ModelConsensus />
          </div>
          <div className={styles.StockNews}>
            <h1 className={styles['StockNews-Header']}>Latest Related News</h1>
            <div className={styles['StockNews-Container']}>
              {stockNews.map((data) => (
                <div className={styles['StockNews-Item']} key={data.title}>
                  <img src={data.thumbnail} alt="Stock News Thumbnail" />
                  <h2>{data.title}</h2>
                  <p>{data.content}</p>
                  <p>{data.date} - {data.source}</p>
                </div>
              ))}
            </div>
          </div>
          {/* //TODO - find text for overlay */}
          <div className={styles['Developer-Info-Div']}>
              <img src='chomba.JPG'></img>
              <div className={styles.Overlay}>
                <h2>Get To Know The Developer</h2>
                <p>Graduate Compter Science student from Loughborough....</p> 
              </div>
          </div>
        </div>
      </main>
    </div>
  );
}
