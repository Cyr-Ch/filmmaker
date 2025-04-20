"use client"

import type React from "react"

import { useState } from "react"
import { Loader2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { ScriptModal } from "@/components/script-modal"
import { VideoPreview } from "@/components/video-preview"

export default function BlogToVideoForm() {
  const [blogContent, setBlogContent] = useState("")
  const [customNotes, setCustomNotes] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [videoReady, setVideoReady] = useState(false)
  const [generatedContent, setGeneratedContent] = useState({
    script: "",
    videoNotes: "",
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // Simulate API call to generate script
    setTimeout(() => {
      setGeneratedContent({
        script: `Here's a generated script based on your blog content:\n\n${blogContent.substring(0, 100)}...\n\nThis is where the rest of your script would be generated.`,
        videoNotes: "",
      })
      setIsLoading(false)
      setIsModalOpen(true)
    }, 1500)
  }

  const handleGenerateVideo = () => {
    setIsModalOpen(false)
    setIsProcessing(true)

    // Simulate video processing
    setTimeout(() => {
      setIsProcessing(false)
      setVideoReady(true)
    }, 3000)
  }

  if (isProcessing) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Processing Your Video</CardTitle>
          <CardDescription>Please wait while we generate your video. This may take a few minutes.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col items-center justify-center py-10">
          <Loader2 className="h-16 w-16 animate-spin text-primary" />
          <p className="mt-4 text-center text-muted-foreground">Our AI is hard at work creating your video...</p>
        </CardContent>
      </Card>
    )
  }

  if (videoReady) {
    return <VideoPreview />
  }

  return (
    <>
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Convert Your Blog to Video</CardTitle>
          <CardDescription>
            Paste your blog content below and add any notes to help generate a better script
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
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
              <Label htmlFor="custom-notes">Notes for Script Generation</Label>
              <Textarea
                id="custom-notes"
                placeholder="Add any specific instructions to help generate a better script..."
                value={customNotes}
                onChange={(e) => setCustomNotes(e.target.value)}
              />
            </div>
          </CardContent>
          <CardFooter>
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating Script...
                </>
              ) : (
                "Generate Video"
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
  )
}
