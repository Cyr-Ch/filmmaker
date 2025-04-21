"use client";

import type React from "react";
import { useState, useEffect, useRef } from "react";
import { Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ScriptModal } from "@/components/script-modal";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Terminal } from "lucide-react";

const POLLING_INTERVAL = 5000; // Check status every 5 seconds

export default function BlogSummaryForm() {
    const [blogContent, setBlogContent] = useState("");
    const [customNotes, setCustomNotes] = useState("");
    const [isLoadingSummary, setIsLoadingSummary] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [generatedContent, setGeneratedContent] = useState({
        script: "",
        videoNotes: "",
    });
    const [isGeneratingVideo, setIsGeneratingVideo] = useState(false);
    const [videoId, setVideoId] = useState<string | null>(null);
    const [videoUrl, setVideoUrl] = useState<string | null>(null);
    const [pollingError, setPollingError] = useState<string | null>(null);
    const pollingIntervalId = useRef<NodeJS.Timeout | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        return () => {
            if (pollingIntervalId.current) {
                clearInterval(pollingIntervalId.current);
            }
        };
    }, []);

    useEffect(() => {
        if (pollingIntervalId.current) {
            clearInterval(pollingIntervalId.current);
            pollingIntervalId.current = null;
        }

        if (videoId && isGeneratingVideo) {
            pollingIntervalId.current = setInterval(async () => {
                try {
                    const response = await fetch(
                        `/api/heygen-video-status?videoId=${videoId}`
                    );
                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(
                            data.error || "Failed to fetch video status"
                        );
                    }

                    console.log("Polling status:", data.status);

                    if (data.status === "completed") {
                        setVideoUrl(data.videoUrl);
                        setIsGeneratingVideo(false);
                        setVideoId(null);
                        setPollingError(null);
                        if (pollingIntervalId.current)
                            clearInterval(pollingIntervalId.current);
                    } else if (data.status === "failed") {
                        setPollingError(
                            data.error || "Video generation failed."
                        );
                        setIsGeneratingVideo(false);
                        setVideoId(null);
                        if (pollingIntervalId.current)
                            clearInterval(pollingIntervalId.current);
                    } else {
                        // Status is likely processing, pending, etc. - continue polling
                    }
                } catch (err: any) {
                    console.error("Polling error:", err);
                    setPollingError(`Polling error: ${err.message}`);
                    setIsGeneratingVideo(false);
                    setVideoId(null);
                    if (pollingIntervalId.current)
                        clearInterval(pollingIntervalId.current);
                }
            }, POLLING_INTERVAL);
        }

        return () => {
            if (pollingIntervalId.current) {
                clearInterval(pollingIntervalId.current);
            }
        };
    }, [videoId, isGeneratingVideo]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoadingSummary(true);
        setError(null);
        setPollingError(null);
        setVideoUrl(null);

        try {
            const response = await fetch("/api/summarize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    content: blogContent,
                    notes: customNotes,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(
                    errorData.error || "Failed to summarize content"
                );
            }

            const data = await response.json();
            setGeneratedContent({
                script: data.summary,
                videoNotes: "",
            });
            setIsLoadingSummary(false);
            setIsModalOpen(true);
        } catch (error: any) {
            console.error("Error summarizing content:", error);
            setError(`Failed to summarize content: ${error.message}`);
            setIsLoadingSummary(false);
        }
    };

    const handleGenerateVideo = async () => {
        setIsModalOpen(false);
        setIsGeneratingVideo(true);
        setPollingError(null);
        setVideoUrl(null);
        setVideoId(null);

        try {
            const response = await fetch("/api/generate-heygen-video", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    script: generatedContent.script,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Failed to start video generation"
                );
            }

            if (data.videoId) {
                setVideoId(data.videoId);
            } else {
                throw new Error("No video ID received from server.");
            }
        } catch (error: any) {
            console.error("Error starting video generation:", error);
            setPollingError(
                `Error starting video generation: ${error.message}`
            );
            setIsGeneratingVideo(false);
        }
    };

    if (videoId || isGeneratingVideo || videoUrl || pollingError) {
        return (
            <Card className="w-full">
                <CardHeader>
                    <CardTitle>Video Generation</CardTitle>
                    <CardDescription>
                        {isGeneratingVideo &&
                            "Your video is being generated by Heygen..."}
                        {videoUrl && "Your video is ready!"}
                        {pollingError && "An error occurred."}
                    </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-col items-center justify-center py-10">
                    {isGeneratingVideo && (
                        <>
                            <Loader2 className="h-16 w-16 animate-spin text-primary" />
                            <p className="mt-4 text-center text-muted-foreground">
                                Please wait, this may take a few minutes. Status
                                checks every {POLLING_INTERVAL / 1000}s.
                            </p>
                        </>
                    )}
                    {videoUrl && (
                        <div className="w-full max-w-2xl">
                            <video
                                controls
                                src={videoUrl}
                                className="w-full rounded-lg"
                            >
                                Your browser does not support the video tag.
                            </video>
                        </div>
                    )}
                    {pollingError && (
                        <Alert variant="destructive" className="w-full">
                            <Terminal className="h-4 w-4" />
                            <AlertTitle>Generation Error</AlertTitle>
                            <AlertDescription>{pollingError}</AlertDescription>
                        </Alert>
                    )}
                </CardContent>
                <CardFooter>
                    <Button
                        variant="outline"
                        onClick={() => {
                            setVideoId(null);
                            setIsGeneratingVideo(false);
                            setVideoUrl(null);
                            setPollingError(null);
                        }}
                    >
                        Generate Another Video
                    </Button>
                </CardFooter>
            </Card>
        );
    }

    return (
        <>
            <Card className="w-full">
                <CardHeader>
                    <CardTitle>Summarize Your Blog & Generate Video</CardTitle>
                    <CardDescription>
                        Paste your blog content to generate a script summary,
                        then generate a video.
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-4">
                        {error && (
                            <Alert variant="destructive">
                                <Terminal className="h-4 w-4" />
                                <AlertTitle>Summarization Error</AlertTitle>
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}
                        <div className="space-y-2">
                            <Label htmlFor="blog-content">Blog Content</Label>
                            <Textarea
                                id="blog-content"
                                placeholder="Paste your blog post here..."
                                className="min-h-[200px]"
                                value={blogContent}
                                onChange={(e) => setBlogContent(e.target.value)}
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="custom-notes">
                                Notes for Summary Generation
                            </Label>
                            <Textarea
                                id="custom-notes"
                                placeholder="Add any specific instructions (e.g., desired tone, key points)..."
                                value={customNotes}
                                onChange={(e) => setCustomNotes(e.target.value)}
                            />
                        </div>
                    </CardContent>
                    <CardFooter>
                        <Button
                            type="submit"
                            className="w-full"
                            disabled={isLoadingSummary || !blogContent}
                        >
                            {isLoadingSummary ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Generating Summary...
                                </>
                            ) : (
                                "Review Script & Generate Video"
                            )}
                        </Button>
                    </CardFooter>
                </form>
            </Card>

            <ScriptModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                content={generatedContent}
                setContent={setGeneratedContent}
                onGenerate={handleGenerateVideo}
            />
        </>
    );
}
