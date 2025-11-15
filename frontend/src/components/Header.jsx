import React from "react";
import { Box, Grid } from "@mui/material";
import SRALogo from "../img/logo_SRA.png";

import logoPUC from "../img/logoPUC.png";
import LogoSRAESCURA from "../img/LOGO_SRA_ESCURA.png";

const Header = () => {
  return (
    <Box
      sx={{
        width: "100%",
        bgcolor: "#0056A3",
        py: 2,
        display: "flex",
        alignItems: "center",
      }}
    >
      <Grid
        container
        justifyContent="space-between"
        alignItems="center"
        px={4}
        spacing={2}
      >
        <Grid item>
          <img src={SRALogo} alt="SRA Logo" height="65" />
        </Grid>
        <Grid item>
          <img src={logoPUC} alt="PUC-Rio Logo" height="65" />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Header;
