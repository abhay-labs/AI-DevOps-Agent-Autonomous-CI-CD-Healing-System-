import { useEffect, useState } from "react";

export default function ScorePanel() {

  const [score, setScore] = useState(null);

  useEffect(() => {

    const eventSource = new EventSource("http://127.0.0.1:8000/stream-logs");

    eventSource.onmessage = (event) => {

      try {

        if (event.data.includes("REAL SCORE")) {

          const jsonPart = event.data.split("→")[1];
          const parsed = JSON.parse(jsonPart.replace(/'/g,'"'));

          setScore(parsed);
        }

      } catch {}

    };

    return () => eventSource.close();

  }, []);

  if (!score) {
    return (
      <div className="bg-[#111827] border border-gray-700 rounded-2xl p-5 shadow-xl">
        <h2 className="text-lg font-semibold text-cyan-400">
          Score Breakdown
        </h2>
        <p className="text-gray-400 mt-3">Waiting for score...</p>
      </div>
    );
  }

  const Bar = ({label,value,color}) => (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span>{label}</span>
        <span className="text-cyan-400">{value}</span>
      </div>
      <div className="w-full bg-[#0B0F19] h-2 rounded">
        <div className={`h-2 rounded ${color}`} style={{width:`${value}%`}} />
      </div>
    </div>
  );

  return (
    <div className="bg-[#111827] border border-gray-700 rounded-2xl p-5 shadow-xl">

      <h2 className="text-lg font-semibold mb-4 text-cyan-400">
        Score Breakdown
      </h2>

      <div className="space-y-4">

        <Bar label="Speed Score" value={score.speed_score} color="bg-cyan-400"/>
        <Bar label="Stability Score" value={score.stability_score} color="bg-purple-400"/>
        <Bar label="Fix Efficiency" value={score.fix_efficiency} color="bg-pink-400"/>
        <Bar label="Test Health" value={score.test_health} color="bg-green-400"/>

      </div>

      <div className="mt-4 text-xs text-gray-400">
        Execution Time: {score.execution_time}s
      </div>

    </div>
  );
}