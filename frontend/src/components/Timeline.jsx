import { useEffect, useState } from "react";

export default function Timeline() {

  const [logs, setLogs] = useState([]);

  useEffect(() => {

    const eventSource = new EventSource("http://127.0.0.1:8000/stream-logs");

    eventSource.onmessage = (event) => {
      setLogs(prev => [...prev, event.data]);
    };

    return () => eventSource.close();

  }, []);

  return (
    <div className="bg-[#111827] border border-gray-700 rounded-2xl p-5 shadow-xl">

      <h2 className="text-lg font-semibold mb-4 text-cyan-400">
        CI/CD Timeline
      </h2>

      <div className="space-y-3 max-h-[350px] overflow-y-auto pr-2">

        {logs.map((log, i) => {

          let color = "border-gray-500";

          if (log.includes("Repo")) color = "border-cyan-400";
          if (log.includes("Language")) color = "border-purple-400";
          if (log.includes("Toolchain")) color = "border-yellow-400";
          if (log.includes("Fix")) color = "border-pink-400";
          if (log.includes("Commit")) color = "border-green-400";
          if (log.includes("CI/CD")) color = "border-orange-400";
          if (log.includes("PASSED")) color = "border-emerald-500";

          return (
            <div key={i} className="flex items-start gap-3">

              <div className={`w-3 h-3 mt-1 rounded-full border-2 ${color}`} />

              <p className="text-sm text-gray-300">
                {log}
              </p>

            </div>
          );
        })}

      </div>

    </div>
  );
}