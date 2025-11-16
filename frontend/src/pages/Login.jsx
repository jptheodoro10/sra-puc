import React, { useState } from "react";
import Header from "../components/Header.jsx";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  RadioGroup,
  FormControlLabel,
  Radio,
  Link,
} from "@mui/material";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import logoSRA from "../img/logo_SRA.png";
import LogoSRAESCURA from "../img/LOGO_SRA_ESCURA.png";

const Login = () => {
  const [form, setForm] = useState({
    matricula: "",
    senha: "",
    tipo: "aluno", // nosso mvp so contempla alunos
  });

  const navigate = useNavigate();
  const [loginError, setLoginError] = useState("");
  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const isValid =
    form.matricula.trim().length > 0 && form.senha.trim().length > 0;

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!isValid) return;
    setLoginError("");

    try {
      // --- 2. Chame sua API do FastAPI ---
      // (Substitua pela URL e lógica da sua API real)
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          matricula: form.matricula,
          senha: form.senha,
        }),
      });

      if (!response.ok) {
        // Se o login falhar (ex: 401 Senha errada)
        throw new Error("Matrícula ou senha inválida.");
      }

      // --- 3. Pegue os dados do usuário da resposta ---
      const userData = await response.json();
      console.log("Resposta do backend:", userData);
      // Ex: userData pode ser { id: 1, nome: "Fulano de Tal", ... }
      localStorage.setItem("authToken", userData.access_token);
      const nomeDoUsuario = userData.nome;
      localStorage.setItem("userName", userData.nome);

      // --- 4. Navegue programaticamente com o nome ---
      // (Assumindo que sua rota é /TelaInicial/:name)
      // (Se sua rota mudou para /Preferencias/:name, apenas ajuste)

      if (userData.has_profile === false) {
        navigate("/Preferencias");
      } else {
        // Se ele JÁ tem perfil, vai direto para o dashboard
        navigate("/dashboard");
      }
    } catch (error) {
      console.error("Erro no login:", error);
      setLoginError(error.message || "Falha ao tentar login.");
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
        width: "100vw",
        overflowX: "hidden",
        bgcolor: "#B0B0B0",
      }}
    >
      <Header />
      <Box
        sx={{
          flexGrow: 1,
          display: "flex",
          justifyContent: "center",
          alignItems: "flex-start",
          bgcolor: "#9aa0a6",
          p: 2,
        }}
      >
        <Paper
          elevation={4}
          sx={{
            width: { xs: "100%" },
            maxWidth: 320,
            bgcolor: "#d9d9d9",
            p: { xs: 3, sm: 4 },
            borderRadius: 1,
            mt: 5,
          }}
        >
          <Box component="form" onSubmit={onSubmit}>
            <Box sx={{ paddingLeft: 5 }}>
              {" "}
              {/* alinha tudo em cima do botao com a esquerda dele*/}
              {/* Matrícula */}
              <Typography fontWeight="600" variant="body1" sx={{ mb: 0.75 }}>
                Login | Matrícula
              </Typography>
              <Box sx={{ mb: 2 }}>
                <TextField
                  size="small"
                  variant="outlined"
                  value={form.matricula}
                  onChange={handleChange("matricula")}
                  sx={{ bgcolor: "#fff", width: "60%" }}
                />
                <Typography
                  variant="caption"
                  sx={{
                    color: "text.secondary",
                    display: "block",
                    mt: "2.5px",
                  }}
                >
                  Sem o digito verificador
                </Typography>
              </Box>
              {/* Senha */}
              <Typography fontWeight="600" variant="body1" sx={{ mb: 0.75 }}>
                Senha
              </Typography>
              <Box sx={{ mb: 2 }}>
                <TextField
                  type="password"
                  size="small"
                  variant="outlined"
                  value={form.senha}
                  onChange={handleChange("senha")}
                  sx={{ bgcolor: "#fff", width: "60%" }}
                />
                <Typography
                  variant="caption"
                  sx={{
                    color: "text.secondary",
                    display: "block",
                    mt: "2.5px",
                  }}
                >
                  A mesma do PUC Online
                </Typography>
              </Box>
              {/* Tipo de Matrícula */}
              <Typography variant="body1" fontWeight="600" sx={{ mb: 0.5 }}>
                Tipo de Matrícula:
              </Typography>
              <RadioGroup
                row={false}
                value={form.tipo}
                onChange={handleChange("tipo")}
                sx={{ mb: 2 }}
              >
                <FormControlLabel
                  value="aluno"
                  control={<Radio size="small" />}
                  label="Aluno"
                />
                <FormControlLabel
                  value="professor"
                  control={<Radio size="small" />}
                  label="Professor"
                />
                <FormControlLabel
                  value="funcionario"
                  control={<Radio size="small" />}
                  label="Funcionário"
                />
              </RadioGroup>
            </Box>

            {/* Botão */}
            <Button
              type="submit"
              //component={RouterLink}
              //to="/Preferencias"
              variant="contained"
              disabled={!isValid}
              sx={{
                textTransform: "none",
                bgcolor: "#2E5C9A",
                ":hover": { bgcolor: "#1E4475" },
                mb: 2,
                mt: 0,
                py: 1,
                fontSize: "1rem",
                paddingLeft: 8,
                paddingRight: 8,
                marginLeft: 5,
              }}
            >
              Efetuar Login
            </Button>
            {loginError && (
              <Typography
                color="error"
                align="center"
                sx={{ mt: 2, fontWeight: 600 }}
              >
                {loginError}
              </Typography>
            )}
          </Box>

          {/* Links de ajuda */}
          {/* --- SEÇÃO DE AJUDA --- */}

          {/* Título da seção, com seu estilo */}
          <Typography
            align="center"
            variant="body2"
            fontWeight="600"
            sx={{ color: "#333", mb: 1 }}
          >
            Esqueceu sua senha do PUC Online?{" "}
            {/* Removi o ':' final para um visual mais limpo */}
          </Typography>

          {/* Container de links, com seu estilo (vertical, centrado) */}
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 0.5, // Mantém seu espaçamento
            }}
          >
            {/* Links de recuperação com o NOVO TEXTO (Sou Aluno) 
    e o SEU ESTILO (cor, sem sublinhado) 
  */}
            <Link
              component="button"
              underline="none"
              sx={{ color: "#2E5C9A" }}
              // onClick={() => navigate('/recuperar/aluno')} {/* Exemplo de ação */}
            >
              Sou Aluno
            </Link>

            <Link
              component="button"
              underline="none"
              sx={{ color: "#2E5C9A" }}
              // onClick={() => navigate('/recuperar/professor')}
            >
              Sou Professor/Funcionario
            </Link>

            {/* ADICIONADO PARA CONSISTÊNCIA com o formulário */}

            {/* Link de Fale Conosco, com seu estilo de 'bold' */}
            <Link
              component="button"
              underline="none"
              sx={{
                color: "#2E5C9A",
                fontWeight: 600, // Seu 'bold'
                marginTop: "8px", // Adiciona um pequeno espaço para separar do grupo
              }}
              // onClick={() => navigate('/fale-conosco')}
            >
              Fale Conosco
            </Link>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};

export default Login;
