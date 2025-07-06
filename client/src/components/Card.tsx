import React from "react";

type Noticia = {
  sitio: string;
  titulo: string;
  imagen: string;
  fecha: string;
  url: string;
  resumen: string;
};

type Props = {
  noticia: Noticia;
};

const NoticiaCard: React.FC<Props> = ({ noticia }) => {
  return (
    <div className="max-w-3xl mx-auto p-4 bg-white shadow-md rounded-2xl border border-gray-200 hover:shadow-lg transition">
      <a href={noticia.url} target="_blank" rel="noopener noreferrer">
        <img
          src={noticia.imagen}
          alt={noticia.titulo}
          className="w-full h-48 object-cover rounded-xl"
        />
      </a>
      <div className="mt-4 space-y-2">
        <div className="text-sm text-gray-500">{noticia.sitio} · {new Date(noticia.fecha).toLocaleDateString()}</div>
        <a href={noticia.url} target="_blank" rel="noopener noreferrer">
          <h2 className="text-xl font-semibold text-gray-800 hover:text-blue-600 transition">
            {noticia.titulo}
          </h2>
        </a>
        <p className="text-gray-700 text-sm">{noticia.resumen}</p>
      </div>
    </div>
  );
};

export default NoticiaCard;
