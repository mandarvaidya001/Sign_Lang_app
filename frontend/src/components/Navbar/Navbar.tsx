import type { ReactNode } from "react";
import { motion } from "motion/react";
import { BookOpen } from "lucide-react";
import { Logo } from "@/components/Logo/Logo";
import { GithubMark } from "@/components/icons/GithubMark";
import { GITHUB_URL, DOCS_URL } from "@/utils/constants";
import { cn } from "@/utils/cn";

interface NavbarProps {
  /** Content rendered on the right side instead of the default GitHub/Docs links. */
  right?: ReactNode;
  className?: string;
}

/**
 * Deliberately sparse: logo on the left, at most two links on the right.
 * No product/pricing/login items — this is a demo, not a marketing site.
 */
export function Navbar({ right, className }: NavbarProps) {
  return (
    <motion.header
      initial={{ opacity: 0, y: -12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className={cn(
        "relative z-10 flex w-full items-center justify-between px-6 py-5 sm:px-10",
        className,
      )}
    >
      <Logo />
      <nav className="flex items-center gap-2">
        {right ?? (
          <>
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-1.5 rounded-full px-3.5 py-2 text-sm text-white/70 transition hover:bg-white/[0.06] hover:text-white"
            >
              <GithubMark className="h-4 w-4" />
              GitHub
            </a>
            <a
              href={DOCS_URL}
              className="flex items-center gap-1.5 rounded-full px-3.5 py-2 text-sm text-white/70 transition hover:bg-white/[0.06] hover:text-white"
            >
              <BookOpen className="h-4 w-4" aria-hidden="true" />
              Documentation
            </a>
          </>
        )}
      </nav>
    </motion.header>
  );
}
