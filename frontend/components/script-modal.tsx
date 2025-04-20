"use client"

import type { Dispatch, SetStateAction } from "react"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

// Update the GeneratedContent interface to remove tone and add videoNotes
interface GeneratedContent {
  script: string
  videoNotes: string
}

interface ScriptModalProps {
  isOpen: boolean
  onClose: () => void
  content: GeneratedContent
  setContent: Dispatch<SetStateAction<GeneratedContent>>
  onGenerate: () => void
}

export function ScriptModal({ isOpen, onClose, content, setContent, onGenerate }: ScriptModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Customize Your Video</DialogTitle>
          <DialogDescription>
            Review and edit the generated script, then add any notes for the video creation process
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="script">Script</Label>
            <Textarea
              id="script"
              className="min-h-[200px]"
              value={content.script}
              onChange={(e) => setContent({ ...content, script: e.target.value })}
            />
            <p className="text-xs text-muted-foreground">Edit the script to match your desired content and flow</p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="video-notes">Notes for Video Generation</Label>
            <Textarea
              id="video-notes"
              placeholder="Add any specific instructions for the video generation (style, pacing, visuals, etc.)..."
              value={content.videoNotes}
              onChange={(e) => setContent({ ...content, videoNotes: e.target.value })}
            />
            <p className="text-xs text-muted-foreground">
              These notes will guide how your video is created from the script
            </p>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={onGenerate}>Generate Video</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
