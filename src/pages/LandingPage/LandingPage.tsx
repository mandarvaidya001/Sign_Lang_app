import { motion } from "motion/react";
import { useNavigate } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { Navbar } from "@/components/Navbar/Navbar";
import { Button } from "@/components/Button/Button";
import { AnimatedBackground } from "@/components/Background/AnimatedBackground";
import { GithubMark } from "@/components/icons/GithubMark";
import { GITHUB_URL } from "@/utils/constants";

/**
 * The application's first screen. Per 02_Hero_Section.md this page's only
 * job is to explain the product in one glance and send the user to mode
 * selection — no camera access, no backend calls, no scrolling.
 */
export function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="relative flex h-svh w-full flex-col overflow-hidden">
      <AnimatedBackground />
      <Navbar />

      <main className="relative z-10 flex flex-1 flex-col items-center justify-center px-6 text-center">
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1, ease: "easeOut" }}
          className="mb-5 font-serif text-lg italic text-[color:var(--color-gradient-highlight)]"
        >
          AI Powered Accessibility
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, scale: 0.94 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
          className="max-w-3xl bg-gradient-to-b from-white to-[color:var(--color-gradient-highlight)] bg-clip-text text-5xl font-medium leading-[1.05] tracking-tight text-transparent sm:text-7xl"
        >
          Sign Language Recognition
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4, ease: "easeOut" }}
          className="mt-6 max-w-xl text-balance text-base text-white/75 sm:text-lg"
        >
          Convert sign language into readable text using real-time
          Artificial Intelligence, Computer Vision, and Deep Learning.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.55, ease: "easeOut" }}
          className="mt-10 flex flex-col items-center gap-3 sm:flex-row"
        >
          <Button
            variant="primary"
            icon={
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-[color:var(--color-accent)] text-white">
                <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
              </span>
            }
            iconTrailing
            onClick={() => navigate("/select-mode")}
          >
            Start Recognition
          </Button>
          <Button
            variant="secondary"
            icon={<GithubMark className="h-4 w-4" />}
            onClick={() => window.open(GITHUB_URL, "_blank", "noreferrer")}
          >
            View Project
          </Button>
        </motion.div>
      </main>
    </div>
  );
}
