import react from "react";
import styles from "./StockReportHeader.module.css";

const currentDate = new Date().toLocaleDateString();

export const StockReportHeader = () => {
    return (
      <div className={styles.stockReportHeader}>
        <div className={styles.companyInfo}>
          <h1 className={styles.companyName}>FTSE100 (FTSE)</h1>
          <p className={styles.sectorIndustry}>Technology / Consumer Electronics</p>
        </div>
        <div className={styles.stockReportInfo}>
          <p className={styles.stockRover}>Stock Rover</p>
          <p className={styles.reportDate}>Stock Report | {currentDate}</p>
        </div>
      </div>
    );
  };
  
  