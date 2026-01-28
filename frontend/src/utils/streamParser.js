import useStreamStore from '../state/streamStore';


const API_BASE = import.meta.env.VITE_API_URL;

const AUTHOR_MAPPING = {
    // ── Visual agents ──
    CoachVisualAgent: 'coach_visual_blocks',
    AnalystVisualAgent: 'analyst_visual_blocks',
    ManagerVisualAgent: 'manager_visual_blocks',
    PlayerImpactVisualAgent: 'player_visual_blocks',
    OpponentVisualAgent: 'opponent_visual_blocks',

    // ── Text agents ──
    CoachAnalysisLLM: 'coach_analysis',
    AnalystAnalysisLLM: 'analyst_analysis',
    PlayerAnalysisLLM: 'player_analysis',
    ManagerAnalysisLLM: 'manager_analysis',
    OpponentAnalysisLLM: 'opponent_analysis',
};

export function startStream(userId, sessionId, message, initialState = {}) {
    const store = useStreamStore.getState();

    store.reset();
    store.setStreaming(true);
    store.setUserId(userId);
    store.setSessionId(sessionId);

    const analysisBuffers = {
        coach_analysis: '',
        analyst_analysis: '',
        player_analysis: '',
        manager_analysis: '',
        opponent_analysis: '',
    };

    store.addLog({
        author: 'SYSTEM',
        text: `Starting analysis for team: ${initialState.team_name || 'Unknown'}`,
    });

    fetch(`${API_BASE}/run/stream`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        body: JSON.stringify({
            user_id: userId,
            session_id: sessionId,
            message,
            initial_state: initialState,
        }),
    })
        .then(async (res) => {
            const reader = res.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const events = chunk.split("\n\n").filter(Boolean);

                for (const evt of events) {
                    if (evt.includes("[DONE]")) {
                        store.addLog({
                            author: 'SYSTEM',
                            text: 'Streaming completed.',
                        });
                        store.setStreaming(false);
                        store.setCsvReady(true);
                        continue;
                    }

                    if (!evt.startsWith("data: ")) continue;

                    try {
                        const payload = JSON.parse(evt.replace("data: ", ""));
                        const { author, text, kind } = payload;

                        if (text == null) continue;

                        const stateKey = AUTHOR_MAPPING[author];

                        /* ─────────────────────────────
                           1️⃣ Structured visual output
                        ───────────────────────────── */
                        if (kind === 'structured' && stateKey) {
                            const parsed =
                                typeof text === 'string'
                                    ? JSON.parse(text)
                                    : text;

                            // 🔥 LOG EVERYTHING STRUCTURED HERE
                            console.group(`[STRUCTURED RESPONSE] ${author}`);
                            console.log('stateKey:', stateKey);
                            console.log('payload:', parsed);
                            console.groupEnd();

                            store.setStructured(stateKey, parsed);

                            // Tab routing (safe)
                            if (stateKey === 'coach_visual_blocks')
                                store.setActiveTab('coach');
                            if (stateKey === 'player_visual_blocks')
                                store.setActiveTab('player');
                            if (stateKey === 'manager_visual_blocks')
                                store.setActiveTab('manager');
                            if (stateKey === 'analyst_visual_blocks')
                                store.setActiveTab('analyst');
                            if (stateKey === 'opponent_visual_blocks')
                                store.setActiveTab('visuals');

                            continue;
                        }

                        /* ─────────────────────────────
                           2️⃣ Streaming text analysis
                        ───────────────────────────── */
                        if (
                            kind === 'text' &&
                            stateKey &&
                            stateKey.endsWith('_analysis') &&
                            typeof text === 'string'
                        ) {
                            analysisBuffers[stateKey] += text;
                            store.setAnalysis(
                                stateKey,
                                analysisBuffers[stateKey]
                            );
                            continue;
                        }

                        /* ─────────────────────────────
                           3️⃣ Logs (ALWAYS FALLBACK)
                        ───────────────────────────── */
                        store.addLog({
                            author: author || 'UNKNOWN',
                            text:
                                typeof text === 'string'
                                    ? text
                                    : JSON.stringify(text),
                        });

                    } catch (err) {
                        console.error("Stream parse error:", err);
                    }
                }
            }
        })
        .catch((err) => {
            console.error("Stream failed:", err);
            store.addLog({
                author: 'SYSTEM',
                text: `Stream error: ${err.message}`,
            });
            store.setStreaming(false);
        });
}
