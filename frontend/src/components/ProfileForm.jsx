import React, { useState } from "react";
import {
  Grid,
  Typography,
  Button,
  Paper,
  Box,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import SelectField from "./SelectField";
import { useNavigate } from "react-router-dom";

const ProfileForm = (props) => {
  const theme = useTheme();
  const isSmall = useMediaQuery(theme.breakpoints.down("sm"));
  const navigate = useNavigate();
  const [form, setForm] = useState({
    curso: "",
    periodo: "",
    formaLecionar: "",
    ritmoAula: "",
    incentivo: "",
    formaAvaliar: "",
    formaLecionarImportancia: "",
    ritmoAulaImportancia: "",
    incentivoImportancia: "",
    formaAvaliarImportancia: "",
  });

  const handleChange = (field) => (event) => {
    setForm({ ...form, [field]: event.target.value });
  };

  const isFormValid = Object.values(form).every((value) => value !== "");

  const handleSubmit = async () => {
    if (!isFormValid) return;

    try {
      // 1. Pegar o token do localStorage
      const token = localStorage.getItem("authToken");
      if (!token) {
        throw new Error("Usuário não autenticado. Faça login novamente.");
      }

      const response = await fetch("http://localhost:8000/aluno/me/perfil", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // adiciona o token de autorização
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Erro ao salvar perfil.");
      }

      navigate("/recomendacoes");
    } catch (err) {
      console.error("Erro ao salvar perfil:", err);
      setError(err.message || "Ocorreu um erro. Tente novamente.");
    }
  };

  // largura fixa padrão para selects
  const selectWidth = { width: 180, minWidth: 180, maxWidth: 180 };
  const selectSmallWidth = { width: 80, minWidth: 80, maxWidth: 80 };

  const userName = localStorage.getItem("userName") || "Usuario";

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        width: "100%",
        px: { xs: 2, sm: 4 },
        py: { xs: 4, md: 6 },
      }}
    >
      <Paper
        elevation={6}
        sx={{
          p: { xs: 2, sm: 3, md: 4 },
          width: "100%",
          maxWidth: 920,
          marginTop: 0,

          mx: "auto",
          borderRadius: 4,
          bgcolor: "#f5f5f5",
          boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
          overflow: "hidden",
          boxSizing: "border-box",
          transition: "none",
        }}
      >
        <Box sx={{ display: "flex", justifyContent: "center" }}>
          <Box sx={{ display: "flex", flexDirection: "column" }}>
            {/* Cabeçalho */}
            <Grid
              container
              mb={6}
              alignItems="center"
              justifyContent="space-between"
            >
              <Grid item>
                <Typography
                  variant="h1"
                  fontWeight="bold"
                  sx={{
                    fontSize: { xs: "1.4rem", md: "1.6rem", xl: "2.0rem" },
                  }}
                >
                  Olá, {userName}! Crie seu perfil!
                </Typography>
              </Grid>
            </Grid>

            {/* Formulário */}
            <Grid
              container
              spacing={6}
              sx={{
                display: "flex",
                flexDirection: "column",
              }}
            >
              {/* Dados Acadêmicos */}
              <Box sx={{ width: "fit-content" }}>
                <Grid item xs={12} md={12}>
                  <Typography
                    variant="h3"
                    mb={2.7}
                    sx={{
                      whiteSpace: "nowrap",
                      fontSize: { xs: "18px", md: "20px", xl: "24px" },
                      fontWeight: 600,
                    }}
                  >
                    Dados Acadêmicos:
                  </Typography>

                  <SelectField
                    required
                    label="Curso"
                    value={form.curso}
                    onChange={handleChange("curso")}
                    options={["Engenharia", "Direito", "Administração"]}
                    selectSx={selectWidth}
                  />
                  <SelectField
                    required
                    label="Período"
                    value={form.periodo}
                    onChange={handleChange("periodo")}
                    options={["1º", "2º", "3º", "4º", "5º", "6º", "7º", "8º"]}
                    selectSx={selectWidth}
                  />
                </Grid>
              </Box>

              {/* Preferências */}
              <Box
                sx={{
                  width: "100%",
                  display: "flex",
                  flexDirection: "column",
                  gap: 2,
                }}
              >
                <Grid item xs={12} md={12}>
                  <Typography
                    variant="h3"
                    mb={-2.5}
                    sx={{
                      fontWeight: 600,
                      whiteSpace: "nowrap",
                      fontSize: { xs: "18px", md: "20px", xl: "24px" },
                    }}
                  >
                    Preferências:
                  </Typography>

                  {/* Colunas: Características e Importância */}
                  <Grid
                    container
                    spacing={2}
                    alignItems="flex-start"
                    justifyContent="flex-start"
                    sx={{
                      flexWrap: { xs: "nowrap", sm: "wrap" },
                      columnGap: { xs: 2, sm: 4 },
                      rowGap: { xs: 1.5, sm: 2 },
                      flexDirection: { xs: "row", sm: "row" },
                    }}
                  >
                    {/* Coluna da esquerda */}
                    <Grid
                      item
                      xs="auto"
                      sm={7}
                      sx={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 1.5,
                        width: "fit-content",
                      }}
                    >
                      {/* Espaçador invisível para alinhar com o título "Importância" da coluna direita */}
                      <Typography
                        variant="subtitle2"
                        sx={{ fontWeight: 600, mb: 1, visibility: "hidden" }}
                      >
                        Importância
                      </Typography>
                      <SelectField
                        required
                        label="Metodologia"
                        value={form.formaLecionar}
                        onChange={handleChange("formaLecionar")}
                        options={["Teórica", "Prática", "Mista"]}
                        selectSx={selectWidth}
                      />
                      <SelectField
                        required
                        label="Ritmo da aula"
                        value={form.ritmoAula}
                        onChange={handleChange("ritmoAula")}
                        options={["Lento", "Moderado", "Rápido"]}
                        selectSx={selectWidth}
                      />
                      <SelectField
                        required
                        label="Participação"
                        value={form.incentivo}
                        onChange={handleChange("incentivo")}
                        options={["Baixo", "Médio", "Alto"]}
                        selectSx={selectWidth}
                      />
                      <SelectField
                        required
                        label="Avaliação"
                        value={form.formaAvaliar}
                        onChange={handleChange("formaAvaliar")}
                        options={["Provas", "Trabalhos", "Projetos"]}
                        selectSx={selectWidth}
                      />
                    </Grid>

                    {/* Coluna da direita (Importância) */}
                    <Grid
                      item
                      xs="auto"
                      sm={4}
                      sx={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 1.5,
                        alignItems: "flex-start",
                        justifyContent: "flex-start",
                        position: "relative",
                        mt: { xs: 0, sm: 0 },
                      }}
                    >
                      <Typography
                        variant="subtitle2"
                        sx={{
                          fontWeight: 600,
                          mb: 1,
                        }}
                      >
                        Importância
                      </Typography>

                      <SelectField
                        required
                        hideLabel
                        value={form.formaLecionarImportancia}
                        onChange={handleChange("formaLecionarImportancia")}
                        options={["1", "2", "3", "4", "5", "6", "7"]}
                        size="small"
                        fullWidth={false}
                        selectSx={selectSmallWidth}
                      />
                      <SelectField
                        required
                        hideLabel
                        value={form.ritmoAulaImportancia}
                        onChange={handleChange("ritmoAulaImportancia")}
                        options={["1", "2", "3", "4", "5", "6", "7"]}
                        size="small"
                        fullWidth={false}
                        selectSx={selectSmallWidth}
                      />
                      <SelectField
                        required
                        hideLabel
                        value={form.incentivoImportancia}
                        onChange={handleChange("incentivoImportancia")}
                        options={["1", "2", "3", "4", "5", "6", "7"]}
                        size="small"
                        fullWidth={false}
                        selectSx={selectSmallWidth}
                      />
                      <SelectField
                        required
                        hideLabel
                        value={form.formaAvaliarImportancia}
                        onChange={handleChange("formaAvaliarImportancia")}
                        options={["1", "2", "3", "4", "5", "6", "7"]}
                        size="small"
                        fullWidth={false}
                        selectSx={selectSmallWidth}
                      />
                    </Grid>
                  </Grid>
                </Grid>
              </Box>
            </Grid>

            {/* Botão */}
            <Grid
              item
              xs={12}
              mt={5}
              sx={{ display: "flex", justifyContent: "center" }}
            >
              <Button
                variant="contained"
                size="large"
                disabled={!isFormValid}
                sx={{
                  textTransform: "none",
                  width: { xs: "100%", sm: "300px" },
                  bgcolor: isFormValid ? "#2860AC" : "#ccc",
                  color: isFormValid ? "white" : "#666",
                  ":hover": {
                    bgcolor: isFormValid ? "#1E4475" : "#ccc",
                    cursor: isFormValid ? "pointer" : "not-allowed",
                  },
                  px: 8,
                  py: 1.2,
                  borderRadius: 3,
                  fontSize: { xs: "1.1rem", md: "1.2rem" },
                }}
                onClick={handleSubmit}
              >
                Salvar Perfil
              </Button>
            </Grid>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default ProfileForm;
