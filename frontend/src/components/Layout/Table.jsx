// =========================
// Reusable Table Component
// =========================
import React from "react";

export function Table({ columns, data, renderActions }) {
  return (
    <div className="bg-white mt-4 rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <table className="w-full text-left table-auto">
        <thead className="bg-slate-50">
          <tr>
            {columns.map((col, i) => (
              <th
                key={i}
                className="p-4 text-sm font-semibold text-slate-600 border-b border-slate-200"
              >
                {col}
              </th>
            ))}
            {renderActions && <th className="p-4">Action</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index} className="hover:bg-slate-50">
              {columns.map((col, i) => (
                <td key={i} className="p-4 border-b border-slate-100">
                  {row[col]}
                </td>
              ))}
              {renderActions && (
                <td className="p-4 border-b border-slate-100">
                  {renderActions(row)}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
