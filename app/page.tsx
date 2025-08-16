import { Suspense } from 'react'
import HeroSection from '@/components/sections/HeroSection'
import FeaturesSection from '@/components/sections/FeaturesSection'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Suspense fallback={<LoadingSpinner />}>
        <HeroSection />
        <FeaturesSection />
      </Suspense>
    </main>
  )
}
