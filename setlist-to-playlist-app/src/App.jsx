import { useState } from "react";
import ArtistSearch from "./components/ArtistSearch";
import SetlistList from "./components/SetlistList";
import SetlistDetail from "./components/SetlistDetail";
import "./App.css";

function App() {
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [selectedSetlist, setSelectedSetlist] = useState(null);
  const [mobileView, setMobileView] = useState("browse");

  const handleSelectSetlist = (setlist) => {
    setSelectedSetlist(setlist);
    setMobileView("detail");
  };

  const handleSelectArtist = (a) => {
    setSelectedArtist(a);
    setSelectedSetlist(null);
    setMobileView("browse");
  };

  return (
    <div className="app-container">
      <div className={`sidebar ${mobileView === "detail" ? "mobile-hidden" : ""}`}>
        <ArtistSearch onSelectArtist={handleSelectArtist} />
        <SetlistList artist={selectedArtist} onSelectSetlist={handleSelectSetlist} />
      </div>
      <div className={`main-content ${mobileView === "browse" ? "mobile-hidden" : ""}`}>
        <SetlistDetail
          setlist={selectedSetlist}
          onBack={() => setMobileView("browse")}
        />
      </div>
    </div>
  );
}

export default App;
