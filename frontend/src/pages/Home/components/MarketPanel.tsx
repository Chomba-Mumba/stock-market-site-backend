import React, { useState, useEffect } from 'react';
import styles from './MarketPanel.module.css';

export const MarketPanel: React.FC = () => {
  const [isMarketOpen, setIsMarketOpen] = useState(false);
  const [nextOpenDate, setNextOpenDate] = useState('');

  // Set your market open/close times 
  const marketOpenTime = 8;
  const marketCloseTime = 16.5; // 4:30 PM


  useEffect(() => {
    const checkMarketStatus = () => {
      const now = new Date();
      const currentHour = now.getHours() + now.getMinutes() / 60;
      const isOpen = currentHour >= marketOpenTime && currentHour <= marketCloseTime && now.getDay() >= 1 && now.getDay() <= 5;
      setIsMarketOpen(isOpen);

      // Calculate the next open date if the market is closed
      if (!isOpen) {
        setNextOpenDate(calculateNextOpenDate(now));
      }
    };

    const calculateNextOpenDate = (date: Date) => {
      const nextDate = new Date(date);
      do {
        nextDate.setDate(nextDate.getDate() + 1);
      } while (nextDate.getDay() === 0 || nextDate.getDay() === 6); // Skip Sunday (0) and Saturday (6)
      
      return formatDate(nextDate);
    };

    const formatDate = (date: Date) => {
      const day = date.getDate();
      const month = date.toLocaleString('en-GB', { month: 'long' });
      const suffix = getDaySuffix(day);
      return `${day}${suffix} ${month}`;
    };

    const getDaySuffix = (day: number) => {
      if (day >= 11 && day <= 13) return 'th';
      switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
      }
    };

    checkMarketStatus();

    // Update market status every minute
    const interval = setInterval(checkMarketStatus, 60000);
    return () => clearInterval(interval);
  }, []);

    const marketMessage = isMarketOpen
    ? "Market open"
    : `Market closed - opens at 08:00 on ${nextOpenDate}`;


  return (
    <div className={styles.marketPanel}>
      <div className={styles.imagePanel}>
        <img src="photo.jpg" alt="IPO Forum Background" className={styles.backgroundImage} />
        <div className={styles.overlayContent}>
          <h1>Stock Market Predictive Model</h1>
          <p>By Chomba Mumba</p>
          <button className={styles.registerButton}>Subscribe to News Letter</button>
        </div>
        <div className={styles.navigation}>
          <button className={styles.arrowLeft}>❮</button>
          <button className={styles.arrowRight}>❯</button>
        </div>
      </div>
      <div className={styles.tickerContainer}>
        <div className={styles.tickerContent}>
            {/* Repeat the market message multiple times for a smooth scrolling effect */}
            {[...Array(10)].map((_, index) => (
            <span key={index} className={styles.tickerItem}>
                {marketMessage}
            </span>
            ))}
        </div>
       </div>
    </div>
  );
};

// TODO get images for Other Market Panels