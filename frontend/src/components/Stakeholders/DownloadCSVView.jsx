import React from 'react';

const API_BASE = "http://localhost:8000";

const DownloadCSVView = () => {
    const downloadCSV = async () => {
        const res = await fetch(`${API_BASE}/download_scouting_data`);
        const blob = await res.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'scouting_data.zip';
        a.click();

        window.URL.revokeObjectURL(url);
    };

    return (
        <div className="h-full flex flex-col items-center justify-center text-center gap-4">
            <div className="text-xl font-mono text-[#e5e7eb]">
                Scouting CSVs Ready
            </div>
            <button
                onClick={downloadCSV}
                className="px-6 py-3 rounded-xl bg-[#e5484d] text-white font-bold uppercase tracking-widest hover:scale-105 transition"
            >
                Download CSV
            </button>
        </div>
    );
};

export default DownloadCSVView;
