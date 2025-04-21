import { NextResponse } from "next/server";

const HEYGEN_API_KEY = process.env.HEYGEN_API_KEY;

const HEYGEN_API_URL = "https://api.heygen.com/v2/video/generate";

// Default values - consider making these configurable if needed
const AVATAR_ID = "Brandon_expressive_public"; // As requested
const VOICE_ID = "fabf3d28753a4d7691d51bbf87d697fb";

export async function POST(request: Request) {
    // Remove diagnostic log as key is now hardcoded
    // console.log("Checking HEYGEN_API_KEY in generate route:", HEYGEN_API_KEY ? `Loaded (length: ${HEYGEN_API_KEY.length})` : "MISSING or undefined");

    if (!HEYGEN_API_KEY) {
        // This check is technically redundant now but kept for structure
        return NextResponse.json(
            { error: "Server configuration error: Heygen API key not found." },
            { status: 500 }
        );
    }

    try {
        const { script } = await request.json();

        if (!script || typeof script !== "string") {
            return NextResponse.json(
                {
                    error: "Bad Request: script is required and must be a string.",
                },
                { status: 400 }
            );
        }

        // Basic check - Heygen likely has stricter limits
        if (script.length > 1500) {
            console.warn(
                "Script length might exceed Heygen limit (1500 chars)."
            );
            // Consider truncating or rejecting if needed
        }

        const response = await fetch(HEYGEN_API_URL, {
            method: "POST",
            headers: {
                "X-Api-Key": HEYGEN_API_KEY,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                video_inputs: [
                    {
                        character: {
                            type: "avatar",
                            avatar_id: AVATAR_ID,
                            avatar_style: "normal", // Can adjust if needed
                        },
                        voice: {
                            type: "text",
                            input_text: script,
                            voice_id: VOICE_ID,
                            // speed: 1.1, // Optional speed adjustment
                        },
                    },
                ],
                dimension: {
                    // Default to 720p as per docs free tier limit
                    width: 1280,
                    height: 720,
                },
                // test: true, // Set to true for testing without using credits (if supported)
                // callback_id: 'your-internal-tracking-id', // Optional
            }),
        });

        const responseData = await response.json();

        if (!response.ok) {
            console.error("Heygen API Error Response:", responseData);
            // Attempt to parse specific error message from Heygen if available
            const errorMessage =
                responseData?.message ||
                `Heygen API Error: ${response.status} ${response.statusText}`;
            return NextResponse.json(
                { error: errorMessage },
                { status: response.status }
            );
        }

        // Assuming the video_id is nested under data -> video_id
        // Adjust this based on actual Heygen response structure
        const videoId = responseData?.data?.video_id;

        if (!videoId) {
            console.error(
                "Could not extract video_id from Heygen response:",
                responseData
            );
            return NextResponse.json(
                {
                    error: "Failed to start video generation job: No video ID received.",
                },
                { status: 500 }
            );
        }

        return NextResponse.json({ videoId: videoId });
    } catch (error) {
        console.error("Error in /api/generate-heygen-video:", error);
        return NextResponse.json(
            { error: "Internal Server Error" },
            { status: 500 }
        );
    }
}
