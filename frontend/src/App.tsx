import { Navigate, Route, Routes } from "react-router-dom";
import { LandingPage } from "@/pages/LandingPage/LandingPage";
import { ModeSelection } from "@/pages/ModeSelection/ModeSelection";
import { Recognition } from "@/pages/Recognition/Recognition";

/**
 * Three screens only, matching 02_Website_Requirements.md exactly:
 * Landing -> Mode Selection -> Live Recognition. Anything else redirects
 * back to the landing page rather than 404ing.
 */
function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/select-mode" element={<ModeSelection />} />
      <Route path="/recognition/:mode" element={<Recognition />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
