import React from 'react';
import styles from './ModelConsensus.module.css';

export function ModelConsensus() {
  const modelSummary = "The model predicts a steady growth in the FTSE100 index over the next month, with a projected average price of $175.00 and a confidence interval of $160 - $190.";
  const predictionRationale = "The model is based on a combination of historical data, sentiment analysis, and technical indicators. The historical data shows a strong correlation between the FTSE100 index and the performance of the technology and consumer electronics sectors. The sentiment analysis indicates a positive outlook for the market, with a high level of confidence in the current trend. The technical indicators suggest that the market is currently in an uptrend, with strong support at the $160 level. Based on this analysis, the model predicts a steady growth in the FTSE100 index over the next month.";
  const historicalAccuracy = 92;
  const sentimentAnalysis = 85;
  return (
    <div className={styles.ModelConsensus}>
      <div className={styles["ModelConsensus-header"]}>
        <h1>Model Consensus</h1>
      </div>
      <div className={styles.PredictionsSummary}>
        <p>{predictionRationale + " " + modelSummary}</p>
        <p>Historical accuracy: {historicalAccuracy}% over the last year</p>
        <p>Sentiment Analysis: {sentimentAnalysis}% over the last year</p>
      </div>
    </div>
  );
}
