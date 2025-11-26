import { Box, Typography } from "@mui/material";
import RecommendationCard from "./RecommendationCard";

const RecommendationList = ({
  recommendations = [],
  selectedSubjectName = "",
}) => {
  if (!recommendations.length) {
    return (
      <Box
        sx={{
          mt: 4,
          textAlign: "center",
          color: "rgba(0,0,0,0.54)",
        }}
      >
        <Typography variant="body1">
          Selecione uma matéria e clique em “Obter Recomendação” para visualizar
          os professores ideais.
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 3, mt: 4 }}>
      {recommendations.map((item, idx) => (
        <RecommendationCard
          key={item.id_professor || idx}
          index={idx + 1}
          nome={item.nome}
          especialidade={selectedSubjectName}
          estrelas={item.estrelas}
        />
      ))}
    </Box>
  );
};

export default RecommendationList;
