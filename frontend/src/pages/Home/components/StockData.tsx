import React from "react";
import styles from "./StockData.module.css";

export const StockData: React.FC = () => {
  // Define the stock metrics directly within the component
  const currentPrice = 169.3;
  const priceChange = -0.59;
  const priceChangePercent = -0.35;
  const yesterday = "Friday";

  return (
    <div className={styles.stockDataContainer}>
      <div className={styles.priceSection}>
        <p className={styles.currentPrice}>${currentPrice.toFixed(2)}</p>
        <p className={styles.priceChange}>
          ${priceChange.toFixed(2)} ({priceChangePercent.toFixed(2)}%)
        </p>
        <p className={styles.priceDate}>as of {yesterday}'s close</p>
      </div>
    </div>
  );
};
