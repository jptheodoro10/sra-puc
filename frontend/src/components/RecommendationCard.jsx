import React from "react";
import { Box, Paper, Typography } from "@mui/material";
import StarRoundedIcon from "@mui/icons-material/StarRounded";
import StarOutlineRoundedIcon from "@mui/icons-material/StarOutlineRounded";
import { colors } from "../constants/recommendationColors";

const TOTAL_STARS = 5;

const RecommendationCard = ({
  index = 0,
  nome = "",
  especialidade = "",
  estrelas = 0,
}) => {
  const filledStars = Math.max(0, Math.min(TOTAL_STARS, Math.round(estrelas)));

  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        borderRadius: 3,
        display: "flex",
        alignItems: "center",
        gap: 2.5,
        border: "1px solid rgba(10,77,173,0.12)",
        boxShadow: "0px 14px 45px rgba(10,77,173,0.08)",
        bgcolor: "#fff",
      }}
    >
      <Box
        sx={{
          width: 54,
          height: 54,
          borderRadius: "50%",
          bgcolor: colors.numberCircleBlue,
          color: "#fff",
          fontWeight: 700,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "1.2rem",
        }}
      >
        {index}
      </Box>

      <Box sx={{ flex: 1 }}>
        <Typography
          variant="h6"
          sx={{ color: colors.primaryTextBlue, fontWeight: 700, mb: 0.5 }}
        >
          {nome}
        </Typography>
        <Typography
          variant="body2"
          sx={{ color: colors.secondaryTextGray, mb: 1 }}
        >
          Especialista em {especialidade}
        </Typography>
        <Box sx={{ display: "flex", gap: 0.5 }}>
          {Array.from({ length: TOTAL_STARS }).map((_, idx) =>
            idx < filledStars ? (
              <StarRoundedIcon
                key={`star-${idx}`}
                sx={{ color: colors.starGreen, fontSize: 28 }}
              />
            ) : (
              <StarOutlineRoundedIcon
                key={`star-${idx}`}
                sx={{ color: colors.starGreen, opacity: 0.3, fontSize: 28 }}
              />
            )
          )}
        </Box>
      </Box>
    </Paper>
  );
};

export default RecommendationCard;
