import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import Papa from "papaparse";

const Card = ({ children }) => (
  <div className="bg-white rounded-xl shadow p-4 mb-6 border">{children}</div>
);
const CardContent = ({ children }) => <div>{children}</div>;

const EcgWaveform = () => {
  const [plotData, setPlotData] = useState({
    sdnn: [],
    rmssd: [],
    lf_hf: [],
    hr: [],
    date: [],
    bpm: [],
    classification: [],
    risk_flag: [],
  });

  useEffect(() => {
    Papa.parse("/ecg_risk_scores_final.csv", {
      download: true,
      header: true,
      complete: (results) => {
        const data = results.data;
        setPlotData({
          sdnn: data.map((row) => parseFloat(row.sdnn)),
          rmssd: data.map((row) => parseFloat(row.rmssd)),
          lf_hf: data.map(
            (row) => parseFloat(row.lf_power) / parseFloat(row.hf_power)
          ),
          hr: data.map((row) => parseFloat(row.avg_hr_bpm)),
          date: data.map((row) => row.recorded_date),
          bpm: data.map((row) => parseFloat(row.avg_hr_bpm)),
          classification: data.map((row) => row.classification),
          risk_flag: data.map((row) => row.risk_flag),
        });
      },
    });
  }, []);

  return (
    <div className="px-4 md:px-12 py-8">
      <h2 className="text-2xl font-bold mb-6">📈 ECG Visualization Module</h2>

      <Card>
        <CardContent>
          <h3 className="text-lg font-semibold mb-2">❤️ Animated ECG Viewer</h3>
          <p className="text-sm text-gray-600 mb-2">
            Displays animated filtered ECG waveform with R-peak overlays to help
            identify electrical activity and heartbeat timing. Useful for
            analyzing arrhythmias or irregular waveforms.
          </p>
          <img
            src="/ecg_animation_record0.gif"
            alt="Animated ECG"
            className="rounded-xl border shadow w-full max-w-3xl"
          />
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h3 className="text-lg font-semibold mb-2">
            📊 Clinical Insights from ECG Trends
          </h3>
          <ul className="list-disc pl-5 text-sm mb-4">
            <li>
              <strong>SDNN vs RMSSD:</strong> Visualizes heart rate variability
              (HRV). High SDNN & RMSSD imply strong parasympathetic regulation;
              lower values suggest possible autonomic imbalance or stress.
            </li>
            <li>
              <strong>LF/HF Ratio vs Avg Heart Rate:</strong> Highlights
              sympathetic vs parasympathetic dominance. Ratios & HR distribution
              help assess physical fatigue or recovery.
            </li>
            <li>
              <strong>ECG Classification vs Heart Rate:</strong> Temporal trends
              showing how heart rhythm types (e.g., Sinus Rhythm, AFib) relate
              to average BPM over time.
            </li>
          </ul>
          <img
            src="/sdnn_vs_rmssd.png"
            alt="SDNN vs RMSSD"
            className="rounded-xl border shadow w-full max-w-4xl mb-4"
          />
          <img
            src="/lfhf_vs_hr.png"
            alt="LF/HF Ratio vs Heart Rate"
            className="rounded-xl border shadow w-full max-w-4xl mb-4"
          />
          <img
            src="/ecg_classification_vs_hr.png"
            alt="ECG Classification vs Heart Rate"
            className="rounded-xl border shadow w-full max-w-4xl mb-4"
          />
          <img
            src="/waveform_rpeaks_panel.png"
            alt="Waveform Plots with R-Peaks"
            className="rounded-xl border shadow w-full max-w-4xl"
          />
        </CardContent>
      </Card>
    </div>
  );
};

export default EcgWaveform;
