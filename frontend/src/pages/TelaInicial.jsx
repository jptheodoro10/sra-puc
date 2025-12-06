import React from "react";
import { Box, Grid } from "@mui/material";
import Header from "../components/Header";
import ProfileForm from "../components/ProfileForm";
import { useParams } from "react-router-dom";

const TelaInicial = () => {
  const params = useParams();
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
        width: "100vw", // garante largura total da viewport
        overflowX: "hidden", // evita barra branca lateral
        bgcolor: "#B0B0B0",
      }}
    >
      <Header showHomeIcon={true} />

      <Grid
        container
        flexGrow={1}
        justifyContent="center"
        alignItems="flex-start"
        sx={{
          flex: 1,
          width: "100%",
          mt: -0, // remove margens automáticas
          px: { xs: 2, sm: 4, md: 6 },
        }}
      >
        <Grid item xs={12} sm={10} md={8} lg={6} xl={5}>
          <ProfileForm name={params.name} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default TelaInicial;
