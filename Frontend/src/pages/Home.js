import React from "react";

const Home = () => {
  return (
    <div className="bg-gray-50 min-h-screen px-6 py-10">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 flex items-center mb-2">
          {" "}
          <span className="ml-2">
            HeartTrend: Data-Driven Health Trends and Lifestyle Nudges
          </span>
        </h1>
        <p className="text-gray-700 mb-6 text-md">
          Objective: Analyze Apple Health and ECG data to generate visual
          insights, detect anomalies, and offer personalized lifestyle nudges.
        </p>

        <div className="bg-white rounded-xl shadow p-6 border mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            🔍 What I Did
          </h2>
          <ul className="list-disc list-inside text-gray-700 space-y-1">
            <li>Parsed and cleaned 46+ Apple Health CSVs</li>
            <li>
              Extracted features and visualized metrics (VO₂ Max, HRV, RHR)
            </li>
            <li>Performed anomaly detection using One-Class SVM, DBSCAN</li>
            <li>Trained LSTM for ECG rhythm classification</li>
            <li>
              Generated LLM-based weekly nudges using trends with local LLaMA
              model (Ollama)
            </li>
            <li>Deployed interactive dashboards via Tableau Public</li>
          </ul>
        </div>

        <div className="bg-white rounded-xl shadow p-6 border mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            🛠️ Tech Stack
          </h2>
          <ul className="list-disc list-inside text-gray-700 space-y-1">
            <li>Frontend: React, Tailwind CSS</li>
            <li>Data Processing: Python, pandas</li>
            <li>Machine Learning: scikit-learn, TensorFlow (LSTM)</li>
            <li>LLM Integration: LLaMA via Ollama for local inference</li>
            <li>Visualization: Tableau Public</li>
          </ul>
        </div>

        <div className="bg-white rounded-xl shadow p-6 border">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            💡 Skills Demonstrated
          </h2>
          <ul className="list-disc list-inside text-gray-700 space-y-1">
            <li>Time-series data preprocessing and feature engineering</li>
            <li>Machine learning for classification and anomaly detection</li>
            <li>Frontend development with modern UI libraries</li>
            <li>LLM-driven behavior insight generation with local models</li>
            <li>Data storytelling and dashboard embedding</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Home;
