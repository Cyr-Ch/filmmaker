import { NextResponse } from "next/server";

const HEYGEN_API_KEY = process.env.HEYGEN_API_KEY;

const HEYGEN_STATUS_API_URL = "https://api.heygen.com/v1/video_status.get";

export async function GET(request: Request) {
    if (!HEYGEN_API_KEY) {
        return NextResponse.json(
            { error: "Server configuration error: Heygen API key not found." },
            { status: 500 }
        );
    }

    const { searchParams } = new URL(request.url);
    const videoId = searchParams.get("videoId");

    if (!videoId) {
        return NextResponse.json(
            { error: "Bad Request: videoId query parameter is required." },
            { status: 400 }
        );
    }

    const url = `${HEYGEN_STATUS_API_URL}?video_id=${videoId}`;

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "X-Api-Key": HEYGEN_API_KEY,
                Accept: "application/json",
            },
            cache: "no-store", // Ensure fresh data is fetched each time
        });

        const responseData = await response.json();

        if (!response.ok) {
            console.error("Heygen Status API Error Response:", responseData);
            const errorMessage =
                responseData?.message ||
                `Heygen Status API Error: ${response.status} ${response.statusText}`;
            // Special handling for 404 which might mean the video ID is wrong or not yet available
            const status = response.status === 404 ? 404 : 500;
            return NextResponse.json(
                { error: errorMessage },
                { status: status }
            );
        }

        // Extract relevant data based on documentation examples
        const status = responseData?.data?.status;
        const videoUrl = responseData?.data?.video_url; // Only present when completed
        const errorMessage = responseData?.data?.error_message; // Present on failure

        if (!status) {
            console.error(
                "Could not determine status from Heygen response:",
                responseData
            );
            return NextResponse.json(
                {
                    error: "Failed to get video status: Invalid response from Heygen.",
                },
                { status: 500 }
            );
        }

        return NextResponse.json({
            status: status,
            videoUrl: videoUrl || null, // Return null if not completed
            error: errorMessage || null, // Return null if no error reported
        });
    } catch (error) {
        console.error("Error in /api/heygen-video-status:", error);
        return NextResponse.json(
            { error: "Internal Server Error" },
            { status: 500 }
        );
    }
}
