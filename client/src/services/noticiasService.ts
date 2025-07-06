import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export type Noticia = {
  sitio: string;
  titulo: string;
  imagen: string;
  fecha: string;
  url: string;
  resumen: string;
};

export async function fetchNoticiasPorCategoria(
  modo: string
): Promise<Noticia[]> {
  try {
    const response = await axios.get(`${API_BASE_URL}/noticias`, {
      params: { modo },
    });
    return response.data;
  } catch (error) {
    console.error("Error al obtener noticias por categoría:", error);
    throw error;
  }
}

export async function buscarNoticias(
  q: string,
  fromdate: string,
  todate: string,
  page = "1",
  top = "12",
  orderby = "creationdate desc"
): Promise<Noticia[]> {
  try {
    const response = await axios.get(`${API_BASE_URL}/busqueda`, {
      params: {
        q,
        fromdate,
        todate,
        page,
        top,
        orderby,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error al buscar noticias:", error);
    throw error;
  }
}
