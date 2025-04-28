import Link from "next/link"
import Image from "next/image"
import { ArrowRight, Database, Shield } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative h-screen flex flex-col items-center justify-center overflow-hidden">
        {/* Background Effect */}
        <div className="absolute inset-0 z-0">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-green-100/50 via-white to-white" />
          <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-green-500/5 blur-3xl rounded-full" />
          <div className="absolute bottom-0 left-0 w-1/2 h-1/2 bg-green-500/5 blur-3xl rounded-full" />
        </div>

        {/* Content - Update text colors from white to black */}
        <div className="container relative z-10 px-4 md:px-6 space-y-12 text-center">
          <div className="space-y-4">
            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter text-black">
              <span className="text-green-600">Bovine</span> Biometric{" "}
              <span className="text-green-600">Identification</span>
            </h1>
            <p className="max-w-[800px] mx-auto text-lg md:text-xl text-gray-700">
              Our advanced AI system uses unique muzzle patterns to identify and track cattle with 99.8% accuracy,
              providing secure identification for insurance claims and livestock management.
            </p>
          </div>

          {/* Animated Cow Muzzle Graphic */}
          <div className="relative w-full max-w-md mx-auto h-48 my-8">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-32 h-32 md:w-40 md:h-40 rounded-full bg-gradient-to-r from-green-500 to-green-700 opacity-70 animate-pulse" />
            </div>
            <div className="absolute inset-0 flex items-center justify-center">
              <Image
                src="/placeholder.svg?height=160&width=160"
                width={160}
                height={160}
                alt="Cow Muzzle Pattern"
                className="rounded-full border-4 border-white/20"
              />
            </div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-full h-full max-w-[200px] max-h-[200px] rounded-full border border-green-500/30 animate-[spin_20s_linear_infinite]" />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="group relative overflow-hidden rounded-lg bg-gradient-to-br from-green-600 to-green-800 px-8 py-4 text-white shadow-lg transition-all hover:shadow-green-500/20 hover:from-green-500 hover:to-green-700"
            >
              <span className="relative z-10 flex items-center justify-center gap-2 text-lg font-medium">
                Register a Cow
                <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
              </span>
              <span className="absolute inset-0 z-0 bg-gradient-to-br from-green-500 to-green-700 opacity-0 transition-opacity group-hover:opacity-100" />
            </Link>

            <Link
              href="/claim"
              className="group relative overflow-hidden rounded-lg bg-black border border-green-500/50 px-8 py-4 text-white shadow-lg transition-all hover:shadow-green-500/20 hover:bg-green-950/30"
            >
              <span className="relative z-10 flex items-center justify-center gap-2 text-lg font-medium">
                Claim Insurance
                <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
              </span>
              <span className="absolute inset-0 z-0 bg-gradient-to-br from-green-950 to-black opacity-0 transition-opacity group-hover:opacity-100" />
            </Link>
          </div>
        </div>

        {/* Keep the rest of the hero section but update the scroll indicator color */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex flex-col items-center text-gray-500">
          <span className="text-sm">Scroll to learn more</span>
          <div className="mt-2 w-1 h-8 bg-gradient-to-b from-green-500 to-transparent rounded-full animate-pulse" />
        </div>
      </div>

      {/* Features Section - Update background and text colors */}
      <div className="bg-white py-24">
        <div className="container px-4 md:px-6 mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-black mb-12">
            Advanced <span className="text-green-600">Biometric</span> Technology
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl border border-green-500/10 hover:border-green-500/30 transition-all shadow-sm">
              <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center mb-4">
                <Database className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-black mb-2">Secure Database</h3>
              <p className="text-gray-600">Encrypted storage of unique muzzle patterns with blockchain verification.</p>
            </div>

            <div className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl border border-green-500/10 hover:border-green-500/30 transition-all shadow-sm">
              <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-black mb-2">Fraud Prevention</h3>
              <p className="text-gray-600">AI-powered verification system prevents fraudulent insurance claims.</p>
            </div>

            <div className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl border border-green-500/10 hover:border-green-500/30 transition-all shadow-sm">
              <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center mb-4">
                <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-black mb-2">Instant Verification</h3>
              <p className="text-gray-600">Real-time matching algorithm provides immediate identification results.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
