import React from "react";
import {
  Avatar,
  Box,
  Button,
  CircularProgress,
  FormControl,
  MenuItem,
  Paper,
  Select,
  Typography,
} from "@mui/material";
import { colors } from "../constants/recommendationColors";
import REX_IMAGE from "../img/Cachorro_mascote 1.png";

const RexCard = ({
  subjects = [],
  selectedSubject = "",
  onSubjectChange,
  onSubmit,
  loading = false,
  errorMessage = "",
  userName = "Aluno",
}) => {
  const handleChange = (event) => {
    onSubjectChange?.(event.target.value);
  };

  return (
    <Paper
      elevation={0}
      sx={{
        width: "100%",
        maxWidth: 420,
        bgcolor: "#fff",
        p: { xs: 3, md: 4 },
        borderRadius: 4,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 3,
        boxShadow: "0 25px 60px rgba(0, 86, 163, 0.12)",
      }}
    >
      <Avatar
        src={REX_IMAGE}
        alt="Rex"
        sx={{
          width: 140,
          height: 140,
          border: `6px solid ${colors.headerBlue}`,
          boxShadow: "0 15px 35px rgba(10,77,173,0.35)",
        }}
      />

      <Box textAlign="center">
        <Typography
          variant="h5"
          sx={{
            color: colors.primaryTextBlue,
            fontWeight: 700,
            mb: 1.5,
            lineHeight: 1.3,
            textTransform: "capitalize",
          }}
        >
          Olá {userName}! Sou o Rex! Pronto para descobrir o professor perfeito
          para você?
        </Typography>
        <Typography
          variant="body1"
          sx={{ color: colors.secondaryTextGray, maxWidth: 320, mx: "auto" }}
        >
          Selecione a matéria para obter a recomendação personalizada
        </Typography>
      </Box>

      <FormControl fullWidth>
        <Select
          value={selectedSubject}
          onChange={handleChange}
          displayEmpty
          sx={{
            borderRadius: 3,
            bgcolor: "#F7F8FC",
            "& .MuiSelect-select": {
              py: 1.5,
            },
          }}
          renderValue={(selected) =>
            selected
              ? subjects.find((subject) => subject.id === selected)?.label
              : "Selecione uma matéria…"
          }
        >
          <MenuItem disabled value="">
            Selecione uma matéria…
          </MenuItem>
          {subjects.map((subject) => (
            <MenuItem key={subject.id} value={subject.id}>
              {subject.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Button
        variant="contained"
        fullWidth
        disabled={!selectedSubject || loading}
        onClick={onSubmit}
        sx={{
          textTransform: "none",
          bgcolor: colors.buttonBlue,
          borderRadius: 3,
          py: 1.6,
          fontSize: "1rem",
          fontWeight: 600,
          "&:hover": {
            bgcolor: "#0D5CBD",
          },
        }}
      >
        {loading ? (
          <CircularProgress size={24} sx={{ color: "#fff" }} />
        ) : (
          "Obter Recomendação"
        )}
      </Button>

      {errorMessage && (
        <Typography variant="body2" color="error">
          {errorMessage}
        </Typography>
      )}
    </Paper>
  );
};

export default RexCard;
