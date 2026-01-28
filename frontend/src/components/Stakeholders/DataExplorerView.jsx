import useStreamStore from '../../state/streamStore';

const DataExplorerView = () => {
    const dataframes = useStreamStore(s => s.dataframes);

    if (!dataframes) {
        return (
            <div className="h-full flex items-center justify-center opacity-40">
                Awaiting data…
            </div>
        );
    }

    return (
        <div className="h-full overflow-auto p-4 space-y-8 font-mono text-sm">
            {Object.entries(dataframes).map(([key, df]) => (
                <div key={key} className="border border-white/10 rounded-xl">
                    <div className="px-4 py-2 bg-[#0b1220] font-bold uppercase tracking-widest text-[#ff4655]">
                        {key} — {df.shape[0]} × {df.shape[1]}
                    </div>

                    <div className="overflow-auto">
                        <table className="min-w-full text-xs">
                            <thead className="bg-[#111827]">
                                <tr>
                                    {df.columns.map(col => (
                                        <th key={col} className="px-3 py-2 text-left">
                                            {col}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {df.rows.map((row, i) => (
                                    <tr key={i} className="border-t border-white/5">
                                        {df.columns.map(col => (
                                            <td key={col} className="px-3 py-1">
                                                {String(row[col])}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default DataExplorerView;
