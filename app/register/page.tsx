"use client"

import type React from "react"

import { useState, useRef } from "react"
import Link from "next/link"
import { ArrowLeft, Upload, Check, X, Play, Pause } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function RegisterPage() {
  const [videoFile, setVideoFile] = useState<File | null>(null)
  const [isRecording, setIsRecording] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [processingStatus, setProcessingStatus] = useState<"idle" | "processing" | "success" | "error">("idle")
  const videoRef = useRef<HTMLVideoElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type.startsWith("video/")) {
      setVideoFile(file)

      // Create a URL for the video file
      const videoUrl = URL.createObjectURL(file)
      if (videoRef.current) {
        videoRef.current.src = videoUrl
      }
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file && file.type.startsWith("video/")) {
      setVideoFile(file)

      // Create a URL for the video file
      const videoUrl = URL.createObjectURL(file)
      if (videoRef.current) {
        videoRef.current.src = videoUrl
      }
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (videoFile) {
      setProcessingStatus("processing")

      // Simulate processing
      setTimeout(() => {
        setProcessingStatus("success")
      }, 3000)
    }
  }

  // Update background and text colors
  return (
    <div className="min-h-screen bg-white text-black">
      <div className="container mx-auto px-4 py-12">
        <Link href="/" className="inline-flex items-center text-green-600 hover:text-green-700 mb-8">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Home
        </Link>

        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold mb-2">Register Your Cow</h1>
          <p className="text-gray-600 mb-8">
            Upload a clear video of your cow's muzzle for our system to register its unique pattern.
          </p>

          <form onSubmit={handleSubmit} className="space-y-8">
            <div
              className={`border-2 border-dashed rounded-xl p-8 text-center ${
                videoFile ? "border-green-500 bg-green-500/5" : "border-gray-300 hover:border-green-500/50"
              } transition-all`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              {!videoFile ? (
                <div className="space-y-4">
                  <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mx-auto">
                    <Upload className="h-8 w-8 text-green-600" />
                  </div>
                  <div>
                    <p className="text-lg font-medium">Drag and drop your video here</p>
                    <p className="text-sm text-gray-600 mt-1">Or click to browse files</p>
                  </div>
                  <Button
                    type="button"
                    variant="outline"
                    className="border-green-500/50 text-green-600 hover:bg-green-500/10"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    Select Video
                  </Button>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="video/*"
                    className="hidden"
                    onChange={handleFileChange}
                  />
                  <p className="text-xs text-gray-500 mt-2">Supported formats: MP4, MOV, AVI (Max 30 seconds)</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="relative max-w-md mx-auto">
                    <video
                      ref={videoRef}
                      className="w-full h-auto rounded-lg border border-green-500/30"
                      controls={false}
                      onEnded={() => setIsPlaying(false)}
                    />
                    <div className="absolute inset-0 flex items-center justify-center">
                      <Button
                        type="button"
                        variant="outline"
                        size="icon"
                        className="bg-white/50 border-green-500/50 text-green-600 hover:bg-green-500/20 rounded-full h-12 w-12"
                        onClick={togglePlay}
                      >
                        {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
                      </Button>
                    </div>
                  </div>
                  <div className="flex justify-center gap-4">
                    <Button
                      type="button"
                      variant="outline"
                      className="border-red-500/50 text-red-500 hover:bg-red-500/10"
                      onClick={() => {
                        setVideoFile(null)
                        setProcessingStatus("idle")
                        if (videoRef.current) {
                          videoRef.current.src = ""
                        }
                      }}
                    >
                      <X className="mr-2 h-4 w-4" />
                      Remove
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      className="border-green-500/50 text-green-600 hover:bg-green-500/10"
                      onClick={() => fileInputRef.current?.click()}
                    >
                      <Upload className="mr-2 h-4 w-4" />
                      Change
                    </Button>
                  </div>
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="cowName" className="text-black">
                  Cow Name
                </Label>
                <Input
                  id="cowName"
                  placeholder="Enter cow name"
                  className="bg-white border-gray-300 focus:border-green-500 text-black"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="cowId" className="text-black">
                  Cow ID/Tag Number
                </Label>
                <Input
                  id="cowId"
                  placeholder="Enter ID or tag number"
                  className="bg-white border-gray-300 focus:border-green-500 text-black"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="breed" className="text-black">
                  Breed
                </Label>
                <Input
                  id="breed"
                  placeholder="Enter breed"
                  className="bg-white border-gray-300 focus:border-green-500 text-black"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="age" className="text-black">
                  Age (Years)
                </Label>
                <Input
                  id="age"
                  type="number"
                  placeholder="Enter age"
                  className="bg-white border-gray-300 focus:border-green-500 text-black"
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-green-600 to-green-800 hover:from-green-500 hover:to-green-700 text-white py-6 text-lg"
              disabled={!videoFile || processingStatus === "processing"}
            >
              {processingStatus === "idle" && "Register Cow"}
              {processingStatus === "processing" && (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Processing...
                </>
              )}
              {processingStatus === "success" && (
                <>
                  <Check className="mr-2 h-5 w-5" />
                  Registration Successful
                </>
              )}
              {processingStatus === "error" && "Registration Failed - Try Again"}
            </Button>
          </form>

          {processingStatus === "success" && (
            <div className="mt-8 p-6 bg-green-500/10 border border-green-500/30 rounded-xl">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <Check className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-medium text-green-600">Registration Successful</h3>
                  <div className="mt-2 text-sm text-gray-700">
                    <p>
                      Your cow has been successfully registered in our system. The unique muzzle pattern has been
                      recorded and can now be used for identification and insurance claims.
                    </p>
                  </div>
                  <div className="mt-4">
                    <Link href="/" className="text-green-600 hover:text-green-700 font-medium">
                      Return to Home
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
