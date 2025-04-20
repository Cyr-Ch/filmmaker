"use client"

import { useState } from "react"
import { Play, Pause, Volume2, VolumeX, Maximize, Minimize } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"

export default function ExampleVideo() {
  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [progress, setProgress] = useState(0)

  const togglePlay = () => {
    setIsPlaying(!isPlaying)
  }

  const toggleMute = () => {
    setIsMuted(!isMuted)
  }

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen)
  }

  return (
    <div className="relative w-full overflow-hidden rounded-lg aspect-video bg-black">
      <video className="w-full h-full object-cover" poster="/placeholder.svg?height=720&width=1280">
        <source
          src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
          type="video/mp4"
        />
        Your browser does not support the video tag.
      </video>

      <div className="absolute inset-0 flex items-center justify-center">
        {!isPlaying && (
          <Button
            variant="ghost"
            size="icon"
            className="h-16 w-16 rounded-full bg-black/30 text-white hover:bg-black/50"
            onClick={togglePlay}
          >
            <Play className="h-8 w-8 fill-current" />
          </Button>
        )}
      </div>

      <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent p-4">
        <div className="space-y-2">
          <Slider
            value={[progress]}
            max={100}
            step={1}
            onValueChange={(value) => setProgress(value[0])}
            className="w-full [&>span:first-child]:h-1.5 [&>span:first-child]:bg-white/30 [&_[role=slider]]:h-3 [&_[role=slider]]:w-3 [&_[role=slider]]:border-0 [&_[role=slider]]:bg-white [&>span:first-child_span]:bg-white"
          />

          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" className="h-8 w-8 text-white" onClick={togglePlay}>
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </Button>

            <Button variant="ghost" size="icon" className="h-8 w-8 text-white" onClick={toggleMute}>
              {isMuted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
            </Button>

            <div className="text-xs text-white">0:45 / 2:30</div>

            <Button variant="ghost" size="icon" className="h-8 w-8 text-white ml-auto" onClick={toggleFullscreen}>
              {isFullscreen ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
