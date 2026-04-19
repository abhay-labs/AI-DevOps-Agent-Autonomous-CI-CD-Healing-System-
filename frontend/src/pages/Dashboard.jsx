import { useState } from "react";
import InputForm from "../components/InputForm";
import RunSummaryCard from "../components/RunSummaryCard";
import ScorePanel from "../components/ScorePanel";
import FixesTable from "../components/FixesTable";
import Timeline from "../components/Timeline";
import AgentThinking from "../components/AgentThinking";

export default function Dashboard() {

  const [runData, setRunData] = useState(null);

  return (
    <div className="min-h-screen bg-[#0B0F19] text-white p-6">

      {/* HEADER */}
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-wide">
          ALPHA DevOps Agent Dashboard
        </h1>
        <div className="text-sm text-cyan-400">
          Autonomous CI/CD Healing Agent
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* LEFT */}
        <div className="lg:col-span-4 space-y-6">
          <InputForm setRunData={setRunData} />
          <RunSummaryCard data={runData} />
          <ScorePanel data={runData} />
        </div>

        {/* RIGHT */}
        <div className="lg:col-span-8 space-y-6">
          <AgentThinking />
          <FixesTable data={runData} />
          <Timeline />
        </div>

      </div>

    </div>
  );
}