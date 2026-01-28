// src/components/OutputPanel.jsx
export default function OutputPanel({ output, sessionState }) {
    return (
        <div>
            <h3>Final Output</h3>
            <pre>{output}</pre>

            <h3>Session State</h3>
            <pre>{JSON.stringify(sessionState, null, 2)}</pre>
        </div>
    );
}
