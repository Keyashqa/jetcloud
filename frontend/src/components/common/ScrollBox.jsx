import React from "react";

const ScrollBox = ({ children, className = "" }) => {
    return (
        <div
            className={`overflow-y-auto scrollbar-thin scrollbar-thumb-valorant-red scrollbar-track-valorant-black ${className}`}
        >
            {children}
        </div>
    );
};

export default ScrollBox;
