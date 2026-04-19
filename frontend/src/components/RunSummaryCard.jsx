export default function RunSummaryCard({ data }) {

  if (!data) {
    return (
      <div className="bg-[#111827] border border-gray-700 rounded-2xl p-5 shadow-xl">
        <h2 className="text-lg font-semibold mb-4 text-cyan-400">
          Run Summary
        </h2>
        <p className="text-gray-400 text-sm">No run yet...</p>
      </div>
    );
  }

  const failures = data.failures?.length || 0;
  const fixes = data.fixes?.length || 0;
  const status = data.status || "FAILED";

  const executionTime = data.score?.execution_time
    ? `${data.score.execution_time}s`
    : "-";

  return (
    <div className="bg-[#111827] border border-gray-700 rounded-2xl p-5 shadow-xl">

      <h2 className="text-lg font-semibold mb-4 text-cyan-400">
        Run Summary
      </h2>

      <p className="text-sm mb-1">Repository: {data.repo_url}</p>
      <p className="text-sm mb-1">Branch: {data.branch || "-"}</p>
      <p className="text-sm mb-1">Total Failures: {failures}</p>
      <p className="text-sm mb-1">Fixes Applied: {fixes}</p>
      <p className="text-sm mb-3">Execution Time: {executionTime}</p>

      <div
        className={`inline-block px-3 py-1 rounded text-sm font-semibold ${
          status === "PASSED"
            ? "bg-green-500 text-black"
            : "bg-red-500 text-white"
        }`}
      >
        {status}
      </div>

    </div>
  );
}