import "./App.css";
import NoticiaCard from "./components/Card";
import NoticiasTabs from "./components/Tabs";

const noticia = {
  sitio: "Pulso SLP",
  titulo: "Notifican a reo nueva orden de aprehensión",
  imagen:
    "https://blobcore.pulsoslp.com.mx/images/2025/07/05/notifican-a-reo-nueva-4b5dae87-focus-0-0-1200-600.webp",
  fecha: "2025-07-05 03:00",
  url: "https://pulsoslp.com.mx/seguridad/notifican-a-reo-nueva-orden-de-aprehension-/1945597",
  resumen:
    "La Policía de Investigación de la Fiscalía General del Estado, notificó en reclusión a Leonel “N” de un nuevo mandamiento judicial en su contra...",
};

function App() {
  return (
    <>
      <div className="min-h-screen bg-gray-50 py-10">
        <NoticiasTabs />
      </div>
    </>
  );
}

export default App;
