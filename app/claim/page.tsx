"use client"

import type React from "react"

import { useState, useRef } from "react"
import Link from "next/link"
import { ArrowLeft, Upload, Check, X, Search, AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function ClaimPage() {
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [verificationStatus, setVerificationStatus] = useState<"idle" | "verifying" | "verified" | "failed">("idle")
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type.startsWith("image/")) {
      setImageFile(file)
      const reader = new FileReader()
      reader.onload = () => {
        setImagePreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file && file.type.startsWith("image/")) {
      setImageFile(file)
      const reader = new FileReader()
      reader.onload = () => {
        setImagePreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (imageFile) {
      setVerificationStatus("verifying")

      // Simulate verification process
      setTimeout(() => {
        // Randomly succeed or fail for demo purposes
        const success = Math.random() > 0.3
        setVerificationStatus(success ? "verified" : "failed")
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
          <h1 className="text-3xl md:text-4xl font-bold mb-2">Claim Insurance</h1>
          <p className="text-gray-600 mb-8">
            Upload a clear image of your registered cow's muzzle for verification and insurance claim processing.
          </p>

          <form onSubmit={handleSubmit} className="space-y-8">
            <div
              className={`border-2 border-dashed rounded-xl p-8 text-center ${
                imageFile ? "border-green-500 bg-green-500/5" : "border-gray-300 hover:border-green-500/50"
              } transition-all`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              {!imageFile ? (
                <div className="space-y-4">
                  <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mx-auto">
                    <Upload className="h-8 w-8 text-green-600" />
                  </div>
                  <div>
                    <p className="text-lg font-medium">Drag and drop your image here</p>
                    <p className="text-sm text-gray-600 mt-1">Or click to browse files</p>
                  </div>
                  <Button
                    type="button"
                    variant="outline"
                    className="border-green-500/50 text-green-600 hover:bg-green-500/10"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    Select Image
                  </Button>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handleFileChange}
                  />
                  <p className="text-xs text-gray-500 mt-2">Supported formats: JPG, PNG, HEIC</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="relative max-w-md mx-auto">
                    {imagePreview && (
                      <img
                        src={imagePreview || "/placeholder.svg"}
                        alt="Cow muzzle preview"
                        className="w-full h-auto rounded-lg border border-green-500/30"
                      />
                    )}

                    {/* Scanning overlay animation when verifying */}
                    {verificationStatus === "verifying" && (
                      <div className="absolute inset-0 overflow-hidden rounded-lg">
                        <div className="absolute inset-0 bg-green-500/10" />
                        <div className="absolute top-0 left-0 w-full h-1 bg-green-500/50 animate-[scan_2s_ease-in-out_infinite]" />
                      </div>
                    )}
                  </div>
                  <div className="flex justify-center gap-4">
                    <Button
                      type="button"
                      variant="outline"
                      className="border-red-500/50 text-red-500 hover:bg-red-500/10"
                      onClick={() => {
                        setImageFile(null)
                        setImagePreview(null)
                        setVerificationStatus("idle")
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
                <Label htmlFor="claimId" className="text-black">
                  Claim ID
                </Label>
                <Input
                  id="claimId"
                  placeholder="Enter claim ID"
                  className="bg-white border-gray-300 focus:border-green-500 text-black"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="cowId" className="text-black">
                  Registered Cow ID/Tag Number
                </Label>
                <Input
                  id="cowId"
                  placeholder="Enter ID or tag number"
                  className="bg-white border-gray-300 focus:border-green-500 text-black"
                />
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="reason" className="text-black">
                  Reason for Claim
                </Label>
                <textarea
                  id="reason"
                  rows={4}
                  placeholder="Describe the reason for your insurance claim"
                  className="w-full bg-white border border-gray-300 focus:border-green-500 text-black rounded-md p-2"
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-green-600 to-green-800 hover:from-green-500 hover:to-green-700 text-white py-6 text-lg"
              disabled={!imageFile || verificationStatus === "verifying"}
            >
              {verificationStatus === "idle" && (
                <>
                  <Search className="mr-2 h-5 w-5" />
                  Verify and Submit Claim
                </>
              )}
              {verificationStatus === "verifying" && (
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
                  Verifying Muzzle Pattern...
                </>
              )}
              {verificationStatus === "verified" && (
                <>
                  <Check className="mr-2 h-5 w-5" />
                  Verification Successful - Submit Claim
                </>
              )}
              {verificationStatus === "failed" && (
                <>
                  <AlertTriangle className="mr-2 h-5 w-5" />
                  Verification Failed - Try Again
                </>
              )}
            </Button>
          </form>

          {verificationStatus === "verified" && (
            <div className="mt-8 p-6 bg-green-500/10 border border-green-500/30 rounded-xl">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <Check className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-medium text-green-600">Verification Successful</h3>
                  <div className="mt-2 text-sm text-gray-700">
                    <p>
                      The muzzle pattern has been successfully matched to a registered cow in our system. Your claim is
                      now ready for processing.
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

          {verificationStatus === "failed" && (
            <div className="mt-8 p-6 bg-red-500/10 border border-red-500/30 rounded-xl">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <AlertTriangle className="h-6 w-6 text-red-500" />
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-medium text-red-500">Verification Failed</h3>
                  <div className="mt-2 text-sm text-gray-700">
                    <p>
                      We couldn't match the muzzle pattern to any registered cow in our system. Please ensure you're
                      uploading a clear image of the correct cow.
                    </p>
                  </div>
                  <div className="mt-4">
                    <Button
                      type="button"
                      variant="outline"
                      className="border-red-500/50 text-red-500 hover:bg-red-500/10"
                      onClick={() => {
                        setImageFile(null)
                        setImagePreview(null)
                        setVerificationStatus("idle")
                      }}
                    >
                      Try Again
                    </Button>
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
