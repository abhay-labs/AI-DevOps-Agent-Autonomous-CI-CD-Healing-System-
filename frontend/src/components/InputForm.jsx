import { useState } from "react";

export default function InputForm({ setResult }) {

  const [repoUrl, setRepoUrl] = useState("");
  const [team, setTeam] = useState("");
  const [leader, setLeader] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const runAgent = async () => {

    if (!repoUrl || !team || !leader) {
      setErrorMsg("⚠️ Please fill all fields before running the agent.");
      return;
    }

    setErrorMsg("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/run-agent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          repo_url: repoUrl,
          team,
          leader
        })
      });

      const data = await res.json();
      setResult(data);

    } catch {
      setErrorMsg("❌ Failed to start agent.");
    }

    setLoading(false);
  };

  return (
    <div className="bg-[#111827] border border-gray-700 rounded-2xl p-5 shadow-xl">

      <h2 className="text-lg font-semibold mb-4 text-cyan-400">
        Analyze Repository
      </h2>

      {errorMsg && (
        <div className="mb-3 p-2 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm animate-pulse">
          {errorMsg}
        </div>
      )}

      <input
        value={repoUrl}
        onChange={(e)=>setRepoUrl(e.target.value)}
        placeholder="GitHub Repo URL"
        className="w-full mb-3 p-2 rounded bg-[#0B0F19] border border-gray-600 focus:border-cyan-400 outline-none"
      />

      <input
        value={team}
        onChange={(e)=>setTeam(e.target.value)}
        placeholder="Team Name"
        className="w-full mb-3 p-2 rounded bg-[#0B0F19] border border-gray-600 focus:border-cyan-400 outline-none"
      />

      <input
        value={leader}
        onChange={(e)=>setLeader(e.target.value)}
        placeholder="Team Leader Name"
        className="w-full mb-4 p-2 rounded bg-[#0B0F19] border border-gray-600 focus:border-cyan-400 outline-none"
      />

      <button
        onClick={runAgent}
        className="w-full bg-cyan-500 hover:bg-cyan-600 transition p-2 rounded-lg font-semibold shadow-[0_0_10px_rgba(0,255,255,0.4)]"
      >
        {loading ? "Running..." : "Run Agent"}
      </button>
    </div>
  );
}
