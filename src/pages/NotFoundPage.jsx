import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="flex flex-col gap-2">
      Erro 404 not found
      <Link to="/"> Voltar a tela Inicial</Link>
      {/*<a href="/"> Home from A</a>*/}
    </div>
  );
}

{
  /* usamos o componente Link para navegar entre paginas pois ele usa cliente-side rotuing.Enquanto o <a> faz a pagina dar refresh e requisita todo o HMTL e o JS denovo, o componente Link transita entre pagines usando c;iente-side routing, evitando que a pagina de refresh, fugindo do efeito de conenxoes lentas e fornecendo uma melhor UX*/
}
