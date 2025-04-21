"use client";

import type { Dispatch, SetStateAction } from "react";

import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

// Update the GeneratedContent interface to reflect summary
interface GeneratedContent {
    script: string;
    videoNotes: string;
}

interface SummaryModalProps {
    isOpen: boolean;
    onClose: () => void;
    content: GeneratedContent;
    setContent: Dispatch<SetStateAction<GeneratedContent>>;
    onGenerate: () => void;
}

export function ScriptModal({
    isOpen,
    onClose,
    content,
    setContent,
    onGenerate,
}: SummaryModalProps) {
    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Review Your Summary</DialogTitle>
                    <DialogDescription>
                        Review and edit the generated summary, then add any
                        notes if needed
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="space-y-2">
                        <Label htmlFor="script">Summary</Label>
                        <Textarea
                            id="script"
                            className="min-h-[200px]"
                            value={content.script}
                            onChange={(e) =>
                                setContent({
                                    ...content,
                                    script: e.target.value,
                                })
                            }
                        />
                        <p className="text-xs text-muted-foreground">
                            Edit the summary to match your desired content
                        </p>
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="video-notes">Additional Notes</Label>
                        <Textarea
                            id="video-notes"
                            placeholder="Add any additional notes or feedback..."
                            value={content.videoNotes}
                            onChange={(e) =>
                                setContent({
                                    ...content,
                                    videoNotes: e.target.value,
                                })
                            }
                        />
                        <p className="text-xs text-muted-foreground">
                            These notes will be saved along with your summary
                        </p>
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button onClick={onGenerate}>Generate Video!</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
