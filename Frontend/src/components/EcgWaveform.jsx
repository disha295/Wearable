import React, { useEffect, useState } from "react";
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
            🧪 Batch R-Peak Visualizer
          </h3>
          <p className="text-sm text-gray-600 mb-2">
            Automatically generates GIFs for high-variance or anomalous ECG
            signals for review. Exported assets are used in clinical dashboards
            and anomaly reports.
          </p>
          <ul className="list-disc pl-5 text-sm">
            <li>Filtered signals parsed using FFT and bandpass filtering</li>
            <li>R-peaks detected from processed RR intervals</li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h3 className="text-lg font-semibold mb-2">
            📊 Clinical Insights from ECG Trends
          </h3>
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

      <Card>
        <CardContent>
          <h3 className="text-lg font-semibold mb-2">🤖 ML Model Evaluation</h3>
          <p className="text-sm text-gray-600 mb-4">
            The ECG classification model was trained on labeled Apple ECG data
            and time-series features extracted from filtered waveforms. Model
            evaluation metrics on the test set are listed below:
          </p>
          <ul className="list-disc pl-5 text-sm mb-4">
            <li>
              <strong>Model:</strong> LSTM (Long Short-Term Memory)
            </li>
            <li>
              <strong>Accuracy:</strong> 100%
            </li>
            <li>
              <strong>Precision:</strong> 1.00
            </li>
            <li>
              <strong>Recall:</strong> 1.00
            </li>
            <li>
              <strong>F1-Score:</strong> 1.00
            </li>
            <li>
              <strong>Classes:</strong> Sinus Rhythm, AFib, Poor Recording
            </li>
          </ul>
          <img
            src="/confusion_matrix.png"
            alt="Confusion Matrix"
            className="rounded-xl border shadow w-full max-w-md"
          />
          <p className="text-xs text-gray-500 mt-2">
            All predictions matched true labels — no false positives or
            negatives detected on holdout data.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default EcgWaveform;
