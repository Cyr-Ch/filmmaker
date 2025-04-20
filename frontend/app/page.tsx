import { Suspense } from "react"
import Link from "next/link"
import { ArrowRight, FileVideo, Loader2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import ExampleVideo from "@/components/example-video"
import BlogToVideoForm from "@/components/blog-to-video-form"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center space-x-4 sm:justify-between sm:space-x-0">
          <div className="flex gap-2 items-center text-xl font-bold">
            <FileVideo className="h-6 w-6" />
            <span>BlogToVideo</span>
          </div>
          <div className="flex flex-1 items-center justify-end space-x-4">
            <nav className="flex items-center space-x-2">
              <Link href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
                Pricing
              </Link>
              <Link href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
                Examples
              </Link>
              <Link href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
                Documentation
              </Link>
              <Button>Sign In</Button>
            </nav>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-b from-muted/50 to-background">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_500px] lg:gap-12 xl:grid-cols-[1fr_550px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                    Transform Your Blog Posts Into Engaging Videos
                  </h1>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    Our AI-powered platform converts your written content into professional videos in minutes. Expand
                    your reach and engage with your audience in a whole new way.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Button size="lg" className="gap-1.5">
                    Get Started <ArrowRight className="h-4 w-4" />
                  </Button>
                  <Button size="lg" variant="outline">
                    View Examples
                  </Button>
                </div>
              </div>
              <div className="mx-auto flex w-full items-center justify-center">
                <Card className="w-full">
                  <CardHeader>
                    <CardTitle>See how it works</CardTitle>
                    <CardDescription>
                      Watch our example video to see the quality of our AI-generated videos
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Suspense
                      fallback={
                        <div className="flex justify-center p-8">
                          <Loader2 className="h-8 w-8 animate-spin" />
                        </div>
                      }
                    >
                      <ExampleVideo />
                    </Suspense>
                  </CardContent>
                  <CardFooter>
                    <p className="text-sm text-muted-foreground">
                      This video was generated from a blog post in just 2 minutes
                    </p>
                  </CardFooter>
                </Card>
              </div>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-2 lg:gap-12">
              <div className="space-y-4">
                <div className="inline-block rounded-lg bg-muted px-3 py-1 text-sm">How It Works</div>
                <h2 className="text-3xl font-bold tracking-tighter md:text-4xl">
                  Three Simple Steps to Create Your Video
                </h2>
                <ul className="grid gap-6">
                  <li className="flex items-start gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
                      1
                    </div>
                    <div className="space-y-1">
                      <h3 className="text-xl font-medium">Paste Your Blog Content</h3>
                      <p className="text-muted-foreground">
                        Simply paste your blog post into our editor and add any custom notes
                      </p>
                    </div>
                  </li>
                  <li className="flex items-start gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
                      2
                    </div>
                    <div className="space-y-1">
                      <h3 className="text-xl font-medium">Customize Your Script</h3>
                      <p className="text-muted-foreground">
                        Review and edit the generated script, tone, and other settings
                      </p>
                    </div>
                  </li>
                  <li className="flex items-start gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
                      3
                    </div>
                    <div className="space-y-1">
                      <h3 className="text-xl font-medium">Download Your Video</h3>
                      <p className="text-muted-foreground">
                        Preview your video in the browser and download it in high quality
                      </p>
                    </div>
                  </li>
                </ul>
              </div>
              <div className="mx-auto w-full max-w-md">
                <BlogToVideoForm />
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="w-full border-t py-6">
        <div className="container flex flex-col items-center justify-center gap-4 md:flex-row md:gap-8">
          <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
            © 2025 BlogToVideo. All rights reserved.
          </p>
          <div className="flex gap-4">
            <Link
              href="#"
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              Terms
            </Link>
            <Link
              href="#"
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              Privacy
            </Link>
            <Link
              href="#"
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
