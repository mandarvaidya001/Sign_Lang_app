import { motion } from "motion/react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Type, BookText, MessageSquare } from "lucide-react";
import { Navbar } from "@/components/Navbar/Navbar";
import { ModeCard } from "@/components/ModeCard/ModeCard";
import { AnimatedBackground } from "@/components/Background/AnimatedBackground";
import type { RecognitionMode } from "@/types";

const MODES: Array<{
  mode: RecognitionMode;
  title: string;
  description: string;
  icon: React.ReactNode;
  available: boolean;
}> = [
  {
    mode: "letter",
    title: "Letter Recognition",
    description: "Recognize individual alphabet gestures.",
    icon: <Type className="h-5 w-5" aria-hidden="true" />,
    available: true,
  },
  {
    mode: "word",
    title: "Word Recognition",
    description: "Recognize predefined words using AI.",
    icon: <BookText className="h-5 w-5" aria-hidden="true" />,
    available: true,
  },
  {
    mode: "sentence",
    title: "Sentence Recognition",
    description: "Recognize complete sentences.",
    icon: <MessageSquare className="h-5 w-5" aria-hidden="true" />,
    available: false,
  },
];

/**
 * Second screen in the flow. Lets the user pick Letter or Word
 * recognition; Sentence recognition is visibly present but inert, per
 * 03_Mode_Selection.md.
 */
export function ModeSelection() {
  const navigate = useNavigate();

  const handleSelect = (mode: RecognitionMode, available: boolean) => {
    if (!available) return;
    navigate(`/recognition/${mode}`);
  };

  return (
    <div className="relative flex h-svh w-full flex-col overflow-hidden">
      <AnimatedBackground subtle />
      <Navbar
        right={
          <button
            type="button"
            onClick={() => navigate("/")}
            className="flex items-center gap-1.5 rounded-full px-3.5 py-2 text-sm text-white/70 transition hover:bg-white/[0.06] hover:text-white"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            Back
          </button>
        }
      />

      <main className="relative z-10 flex flex-1 flex-col items-center justify-center px-6">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="mb-12 text-center"
        >
          <span className="text-xs font-medium uppercase tracking-[0.18em] text-white/40">
            Sign Language Recognition
          </span>
          <h1 className="mt-3 text-3xl font-medium tracking-tight text-white sm:text-4xl">
            Choose a Recognition Mode
          </h1>
        </motion.div>

        <div className="grid w-full max-w-4xl grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {MODES.map((item, i) => (
            <motion.div
              key={item.mode}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.5,
                delay: 0.15 + i * 0.08,
                ease: "easeOut",
              }}
            >
              <ModeCard
                icon={item.icon}
                title={item.title}
                description={item.description}
                available={item.available}
                onSelect={() => handleSelect(item.mode, item.available)}
              />
            </motion.div>
          ))}
        </div>
      </main>
    </div>
  );
}
