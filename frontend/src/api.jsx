// src/api.js
const API_BASE = "http://localhost:8000";

export function streamAgent(payload, onMessage, onDone) {
    const evtSource = new EventSource(
        `${API_BASE}/run/stream`,
        {
            withCredentials: false,
        }
    );

    // Hack: EventSource only supports GET, so we fallback to fetch+ReadableStream
    fetch(`${API_BASE}/run/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    }).then(async (res) => {
        const reader = res.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            chunk
                .split("\n\n")
                .filter(Boolean)
                .forEach((line) => {
                    if (line.includes("[DONE]")) {
                        onDone?.();
                    } else if (line.startsWith("data:")) {
                        const data = JSON.parse(line.replace("data: ", ""));
                        onMessage?.(data);
                    }
                });
        }
    });

    return () => evtSource.close();
}
