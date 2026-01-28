// src/components/StreamPanel.jsx
export default function StreamPanel({ events }) {
    return (
        <div style={{ whiteSpace: "pre-wrap" }}>
            <h3>Live Stream</h3>
            <div>
                {events.map((e, idx) => (
                    <div key={idx}>
                        <strong>{e.author}:</strong> {e.text}
                    </div>
                ))}
            </div>
        </div>
    );
}
