import { useEffect, useRef, useState } from "react";

export default function AgentThinking() {
  const [logs, setLogs] = useState([]);
  const containerRef = useRef(null);

  useEffect(() => {
    const eventSource = new EventSource(
      "http://127.0.0.1:8000/stream-logs"
    );

    eventSource.onmessage = (event) => {
      setLogs((prev) => [...prev, event.data]);
    };

    return () => eventSource.close();
  }, []);

  // ✅ auto scroll
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop =
        containerRef.current.scrollHeight;
    }
  }, [logs]);

  // 🎨 Agent based color system
  const getColor = (log) => {
    if (log.includes("[Repo Agent]")) return "text-cyan-400";
    if (log.includes("[Test Agent]")) return "text-yellow-400";
    if (log.includes("[Fix Agent]")) return "text-purple-400";
    if (log.includes("[CI/CD Agent]")) return "text-green-400";
    return "text-green-300";
  };

  return (
    <div className="bg-black border border-cyan-500/30 rounded-2xl p-4 shadow-[0_0_25px_rgba(0,255,255,0.12)]">

      {/* HEADER */}
      <div className="flex items-center gap-2 mb-3">
        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
        <h2 className="text-cyan-400 text-sm font-semibold tracking-widest">
          LIVE AI AGENT TERMINAL
        </h2>
      </div>

      {/* TERMINAL BODY */}
      <div
        ref={containerRef}
        className="h-64 overflow-y-auto font-mono text-sm space-y-1"
      >
        {logs.map((log, i) => (
          <p
            key={i}
            className={`${getColor(log)} animate-pulse`}
            style={{ textShadow: "0 0 6px currentColor" }}
          >
            {">"} {log}
          </p>
        ))}

        {/* blinking cursor */}
        <span className="text-green-400 animate-pulse">█</span>
      </div>
    </div>
  );
}
