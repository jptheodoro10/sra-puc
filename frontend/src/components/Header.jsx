import React from "react";
import { Avatar, Box, Divider, IconButton, useTheme } from "@mui/material";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import SRALogo from "../img/logo_SRA.png";
import logoPUC from "../img/logoPUC.png";
import { colors } from "../constants/recommendationColors";
import DefaultAvatar from "../img/defaultAvatar.svg";

const Header = ({ avatarLabel = "AL", showUserMenu = false }) => {
  const theme = useTheme();

  return (
    <Box
      component="header"
      sx={{
        width: "100%",
        bgcolor: colors.headerBlue,
        color: "#fff",
        minHeight: 80,
        boxShadow: "0px 6px 14px rgba(0,0,0,0.15)",
        display: "flex",
        alignItems: "center",
        px: { xs: 3, md: 6 },
        py: 1.5,
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          width: "100%",
          justifyContent: "space-between",
          gap: { xs: 2, md: 4 },
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: { xs: 2, sm: 3 },
            flexWrap: "nowrap",
          }}
        >
          <Box
            component="img"
            src={SRALogo}
            alt="SRA logo"
            sx={{ height: { xs: 44, sm: 56 }, width: "auto" }}
          />
          <Divider
            orientation="vertical"
            flexItem
            sx={{
              borderColor: colors.dividerBlue,
              borderRightWidth: 2,
              mx: 0.5,
              height: theme.spacing(6),
            }}
          />
          <Box
            component="img"
            src={logoPUC}
            alt="PUC-Rio logo"
            sx={{ height: { xs: 44, sm: 56 }, width: "auto" }}
          />
        </Box>

        {showUserMenu && (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
            }}
          >
            <Avatar
              src={DefaultAvatar}
              alt="Perfil"
              sx={{
                bgcolor: "#fff",
                width: 52,
                height: 52,
                border: "2px solid rgba(255,255,255,0.6)",
              }}
            >
              {avatarLabel}
            </Avatar>
            <IconButton
              size="small"
              sx={{
                color: "#fff",
                bgcolor: "transparent",
                "&:hover": { bgcolor: "rgba(255,255,255,0.12)" },
              }}
            >
              <ArrowDropDownIcon fontSize="large" />
            </IconButton>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default Header;
