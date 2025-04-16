import { useEffect, useState } from "react";
import Papa from "papaparse";

function Nudges() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/weekly_nudges_llm.csv")
      .then((res) => res.text())
      .then((text) => {
        Papa.parse(text, {
          header: true,
          skipEmptyLines: true,
          complete: ({ data }) => {
            // Filter rows with both fields present
            const filtered = data.filter(
              (row) => row.TrendSummary?.trim() && row.LLM_Nudge?.trim()
            );
            setData(filtered);
          },
        });
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 px-6 py-10">
      <h1 className="text-3xl font-bold mb-8 flex items-center text-gray-800">
        <span className="ml-2">Weekly LLM-Based Nudges</span>
      </h1>

      <div className="space-y-6">
        {data.map((row, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-xl shadow border border-gray-200 hover:shadow-lg transition duration-300"
          >
            <p className="text-sm text-gray-600 mb-1">
              <span className="font-medium text-gray-700">Week:</span>{" "}
              {row.week}
            </p>
            <p className="text-blue-700 font-medium mb-2">
              <span className="font-semibold">Trend:</span>{" "}
              <span className="underline">{row.TrendSummary}</span>
            </p>
            <p className="text-green-700 font-medium">
              <span className="font-semibold">Nudge:</span> {row.LLM_Nudge}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Nudges;
