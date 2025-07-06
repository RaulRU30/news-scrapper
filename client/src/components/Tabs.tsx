import React, { useState, useEffect } from "react";
import {
  fetchNoticiasPorCategoria,
  buscarNoticias,
} from "../services/noticiasService";
import type { Noticia } from "../services/noticiasService";
import NoticiaCard from "./Card";

const tabs = ["San Luis", "Nacional", "Mundo", "Seguridad", "Busqueda"];

const NoticiasTabs: React.FC = () => {
  const [activeTab, setActiveTab] = useState("San Luis");
  const [query, setQuery] = useState("");
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [noticias, setNoticias] = useState<Noticia[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setNoticias([]);
    if (activeTab !== "Busqueda") {
      const modo = convertirTabAModo(activeTab);
      setLoading(true);
      fetchNoticiasPorCategoria(modo)
        .then(setNoticias)
        .catch(() => setError("Error al cargar noticias."))
        .finally(() => setLoading(false));
    }
  }, [activeTab]);

  const convertirTabAModo = (tab: string) => {
    switch (tab) {
      case "San Luis":
        return "slp";
      case "Nacional":
        return "nacional";
      case "Mundo":
        return "mundo";
      case "Seguridad":
        return "seguridad";
      default:
        return "slp";
    }
  };

  const handleBuscar = async () => {
    setLoading(true);
    setError("");
    setNoticias([]);
    try {
      const noticias = await buscarNoticias(query, desde, hasta);
      setNoticias(noticias);
    } catch (err) {
      setError("Error al realizar la búsqueda." + err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-8">Noticias App</h1>

      <div className="flex justify-center flex-wrap gap-3 mb-8">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-5 py-2 rounded-full border text-sm font-medium transition-all duration-200 shadow-sm ${
              activeTab === tab
                ? "bg-green-200 border-green-400 text-green-900"
                : "bg-white border-gray-300 hover:bg-gray-100"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      <div className="bg-white border rounded-2xl shadow-md p-6 min-h-[250px]">
        {activeTab === "Busqueda" ? (
          <div className="flex flex-col items-center space-y-5">
            <input
              type="text"
              placeholder="Ingresa tu búsqueda"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full max-w-md p-3 border rounded-lg shadow-sm text-center"
            />

            <div className="flex gap-4">
              <input
                type="date"
                value={desde}
                onChange={(e) => setDesde(e.target.value)}
                className="p-2 border rounded-md shadow-sm"
              />
              <input
                type="date"
                value={hasta}
                onChange={(e) => setHasta(e.target.value)}
                className="p-2 border rounded-md shadow-sm"
              />
            </div>

            <button
              onClick={handleBuscar}
              className="px-6 py-2 rounded-lg bg-green-500 text-white hover:bg-green-600 transition"
            >
              Buscar
            </button>
          </div>
        ) : null}

        <div className="mt-6">
          {loading ? (
            <p className="text-center text-gray-400">Cargando noticias...</p>
          ) : error ? (
            <p className="text-center text-red-500">{error}</p>
          ) : noticias.length > 0 ? (
            <div className="grid gap-6">
              {noticias.map((noticia, idx) => (
                <NoticiaCard key={idx} noticia={noticia} />
              ))}
            </div>
          ) : (
            <p className="text-center text-gray-500">
              No hay noticias disponibles.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default NoticiasTabs;
