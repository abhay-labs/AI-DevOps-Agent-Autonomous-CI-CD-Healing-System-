export default function FixesTable({ result }) {

  const fixes = result?.fixes || [];

  return (
    <div className="bg-[#111827] border border-gray-700 rounded-2xl p-5 shadow-xl">

      <h2 className="text-lg font-semibold text-cyan-400 mb-4">
        Fixes Applied
      </h2>

      {fixes.length === 0 ? (
        <p className="text-gray-400 text-sm">
          No fixes applied yet.
        </p>
      ) : (

        <div className="overflow-x-auto">

          <table className="w-full text-sm font-mono">

            <thead>
              <tr className="text-gray-400 border-b border-gray-700">
                <th className="text-left pb-2">FILE</th>
                <th className="text-left pb-2">LINE</th>
                <th className="text-left pb-2">TYPE</th>
                <th className="text-left pb-2">FIX DESCRIPTION</th>
              </tr>
            </thead>

            <tbody>
              {fixes.map((fix, i) => (

                <tr key={i} className="border-b border-gray-800 hover:bg-[#0B0F19] transition">

                  <td className="py-2 text-cyan-300">
                    {fix.file || "-"}
                  </td>

                  <td className="py-2">
                    {fix.line || "-"}
                  </td>

                  <td className={`py-2 font-semibold ${
                    fix.type === "AST"
                      ? "text-cyan-400"
                      : "text-purple-400"
                  }`}>
                    {fix.type || "AI"}
                  </td>

                  <td className="py-2 text-gray-300">
                    {fix.description || "Auto Fix Applied"}
                  </td>

                </tr>

              ))}
            </tbody>

          </table>

        </div>
      )}

    </div>
  );
}
