import React, { useEffect, useMemo, useState } from "react";
import { Box, CircularProgress, Grid, Typography } from "@mui/material";
import Header from "../components/Header";
import RexCard from "../components/RexCard";
import RecommendationList from "../components/RecommendationList";
import { colors } from "../constants/recommendationColors";

const resolveApiBaseUrl = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }

  if (typeof window !== "undefined") {
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:8000`;
  }

  return "http://localhost:8000";
};

const RecommendationPage = () => {
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [subjectsLoading, setSubjectsLoading] = useState(true);
  const [error, setError] = useState("");

  const [apiBaseUrl] = useState(() => resolveApiBaseUrl());
  const disciplinasUrl = `${apiBaseUrl}/aluno/disciplinas`;
  const recommendationsUrl = `${apiBaseUrl}/aluno/recomendacoes`;

  const userName =
    typeof window !== "undefined"
      ? localStorage.getItem("userName") || "Aluno"
      : "Aluno";

  const avatarLabel = useMemo(() => {
    const initials = userName
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("");
    return initials || "AL";
  }, [userName]);

  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const token = localStorage.getItem("authToken");
        if (!token) {
          throw new Error(
            "Usuário não autenticado. Faça login para visualizar as matérias."
          );
        }

        const response = await fetch(disciplinasUrl, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const { detail } = await response.json();
          throw new Error(
            detail || "Não foi possível carregar as disciplinas."
          );
        }

        const data = await response.json();
        const parsedSubjects = data.map((disciplina) => ({
          id: Number(disciplina.id_disciplina),
          label: disciplina.nome,
        }));
        setSubjects(parsedSubjects);
        setError("");
      } catch (fetchError) {
        setError(fetchError.message);
      } finally {
        setSubjectsLoading(false);
      }
    };

    fetchSubjects();
  }, [disciplinasUrl]);

  const selectedSubjectName = useMemo(() => {
    return subjects.find((subject) => subject.id === selectedSubjectId)?.label;
  }, [subjects, selectedSubjectId]);

  const preparedRecommendations = useMemo(() => {
    return recommendations.slice(0, 5).map((item) => ({
      ...item,
      estrelas: Math.max(
        0,
        Math.min(
          5,
          Math.round(
            item.estrelas ??
              (typeof item.similaridade === "number"
                ? item.similaridade * 5
                : 0)
          )
        )
      ),
    }));
  }, [recommendations]);

  const handleSubjectChange = (value) => {
    if (value === "" || value === undefined) {
      setSelectedSubjectId("");
      setRecommendations([]);
      setError("");
      return;
    }

    setSelectedSubjectId(Number(value));
    setError("");
  };

  const handleFetchRecommendations = async () => {
    if (!selectedSubjectId) {
      setError("Selecione uma matéria antes de solicitar recomendações.");
      return;
    }

    try {
      const token = localStorage.getItem("authToken");
      if (!token) {
        throw new Error("Sessão expirada. Faça login novamente.");
      }

      setLoadingRecommendations(true);
      setError("");

      const response = await fetch(
        `${recommendationsUrl}?disciplina_id=${selectedSubjectId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        const { detail } = await response.json();
        throw new Error(
          detail ||
            "Não conseguimos gerar as recomendações. Tente novamente em instantes."
        );
      }

      const data = await response.json();
      setRecommendations(data);
    } catch (fetchError) {
      setRecommendations([]);
      setError(fetchError.message);
    } finally {
      setLoadingRecommendations(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: colors.rightBackground,
        display: "flex",
        flexDirection: "column",
        width: "100%",
      }}
    >
      <Header showUserMenu avatarLabel={avatarLabel} showHomeIcon={true} />

      <Box
        sx={{
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          flexGrow: 1,
          width: "100%",
        }}
      >
        {/* ESQUERDA */}
        <Box
          sx={{
            flex: 1,
            bgcolor: colors.leftBackground,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            py: { xs: 6, md: 8 },
            px: { xs: 3, md: 6 },
          }}
        >
          {subjectsLoading ? (
            <CircularProgress sx={{ color: colors.buttonBlue }} />
          ) : (
            <RexCard
              subjects={subjects}
              selectedSubject={selectedSubjectId}
              onSubjectChange={handleSubjectChange}
              onSubmit={handleFetchRecommendations}
              loading={loadingRecommendations}
              errorMessage={error}
              userName={userName}
            />
          )}
        </Box>

        {/* DIREITA */}
        <Box
          sx={{
            flex: 1,
            bgcolor: colors.rightBackground,
            py: { xs: 6, md: 8 },
            px: { xs: 3, md: 6 },
            display: "flex",
            flexDirection: "column",
            alignItems: "center", // centraliza conteúdo
          }}
        >
          {/* Título */}
          <Typography
            variant="h4"
            sx={{
              fontWeight: 700,
              color: colors.primaryTextBlue,
              mb: 1,
              textAlign: "center",
            }}
          >
            Suas Recomendações
          </Typography>

          {/* Mensagem inicial: só aparece enquanto não está carregando
      E ainda não existem recomendações */}
          {!loadingRecommendations && preparedRecommendations.length === 0 && (
            <Typography
              variant="body1"
              sx={{
                color: colors.secondaryTextGray,
                textAlign: "center",
                maxWidth: "600px",
                mx: "auto",
                mb: 4,
              }}
            >
              Selecione uma matéria e clique em “Obter Recomendação” para
              visualizar os professores ideais.
            </Typography>
          )}

          {/* Loading */}
          {loadingRecommendations && (
            <Box
              sx={{
                mt: 4,
                display: "flex",
                justifyContent: "center",
              }}
            >
              <CircularProgress sx={{ color: colors.buttonBlue }} />
            </Box>
          )}

          {/* Lista de recomendações: só aparece quando já terminou de carregar
      E existem recomendações */}
          {!loadingRecommendations && preparedRecommendations.length > 0 && (
            <Box sx={{ mt: -1.5, width: "100%" }}>
              <RecommendationList
                recommendations={preparedRecommendations}
                selectedSubjectName={selectedSubjectName || ""}
              />
            </Box>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default RecommendationPage;
