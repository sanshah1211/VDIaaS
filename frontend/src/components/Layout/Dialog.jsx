
// =========================
// Reusable Dialog Component
// =========================
import React from "react";
export function Dialog({ open, title, children, onClose, onSubmit }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/30 backdrop-blur-sm">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-black"
        >
          ✕
        </button>

        <h2 className="text-xl font-semibold mb-4">{title}</h2>

        <div className="mb-4">{children}</div>

        <div className="flex gap-2">
          <button
            onClick={onSubmit}
            className="bg-slate-800 text-white px-4 py-2 rounded"
          >
            Submit
          </button>
          <button
            onClick={onClose}
            className="border px-4 py-2 rounded"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
