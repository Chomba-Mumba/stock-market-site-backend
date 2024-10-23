import react from "react";
import "./StockReportHeader.module.css";

export const StockReportHeader = () => {
    return (
      <div className="stock-report-header">
        <div className="company-info">
          <h1 className="company-name">Apple (AAPL)</h1>
          <p className="sector-industry">Technology / Consumer Electronics</p>
        </div>
        <div className="stock-report-info">
          <p className="stock-rover">Stock Rover</p>
          <p className="report-date">Stock Report | April 27, 2024</p>
        </div>
      </div>
    );
  };
  
  