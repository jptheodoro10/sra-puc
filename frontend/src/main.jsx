import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./pages/Login.jsx";
import TelaInicial from "./pages/TelaInicial.jsx";
import NotFoundPage from "./pages/NotFoundPage.jsx";
import RecommendationPage from "./pages/RecommendationPage.jsx";
//import TelaPrincipal from "./pages/TelaPrincipal.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Login />,
    errorElement: <NotFoundPage />,
  },
  {
    path: "/Preferencias", //incluir dynamic param
    element: <TelaInicial />,
  },
  {
    path: "/recomendacoes",
    element: <RecommendationPage />,
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
