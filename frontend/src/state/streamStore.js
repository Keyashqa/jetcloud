import { create } from 'zustand';
import managerVisualBlocks from '../components/Stakeholders/mock';
import coachMock from '../components/Stakeholders/coachmock';
import analystMock from '../components/Stakeholders/analystmock';
import opponentMock from '../components/Stakeholders/Opponentmock';
import simulationMock from '../components/Stakeholders/VisualMock';

const useStreamStore = create((set) => ({
    // ===============================
    // Logs 
    // ===============================
    logs: [],

    // ===============================
    // Text analysis outputs
    // ===============================
    coach_analysis: null,
    analyst_analysis: null,
    player_analysis: null,
    manager_analysis: null,

    // ===============================
    // Structured visual outputs
    // ===============================
    coach_visual_blocks: coachMock,
    analyst_visual_blocks: analystMock,
    player_visual_blocks: simulationMock,
    manager_visual_blocks: managerVisualBlocks,
    opponent_visual_blocks: opponentMock,

    // ===============================
    // UI State
    // ===============================
    isStreaming: false,
    csvReady: false,
    activeTab: 'coach',

    userId: 'user_1',
    sessionId: 'session_stream_1',

    dataframes: null,

    // ===============================
    // Actions
    // ===============================

    addLog: (log) =>
        set((state) => ({ logs: [...state.logs, log] })),

    setAnalysis: (key, content) =>
        set(() => ({ [key]: content })),

    setStructured: (key, data) =>
        set(() => ({ [key]: data })),

    setStreaming: (status) =>
        set({ isStreaming: status }),

    setCsvReady: (status) =>
        set({ csvReady: status }),

    setActiveTab: (tab) =>
        set({ activeTab: tab }),

    setSessionId: (id) =>
        set({ sessionId: id }),

    setUserId: (id) =>
        set({ userId: id }),

    setDataframes: (data) =>
        set({ dataframes: data }),



    // ===============================
    // Reset (NEW RUN)
    // ===============================
    reset: () =>
        set({
            logs: [],

            coach_analysis: null,
            analyst_analysis: null,
            player_analysis: null,
            manager_analysis: null,

            coach_visual_blocks: null,
            analyst_visual_blocks: null,
            player_visual_blocks: null,
            manager_visual_blocks: null,
            opponent_visual_blocks: null,

            isStreaming: false,
            csvReady: false,
            activeTab: 'coach',
        }),
}));

export default useStreamStore;
