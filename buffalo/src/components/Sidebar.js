import * as React from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import { Link } from "react-router-dom";

const drawerWidth = 240;

const Sidebar = () => {
  return (
    <Box>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
        variant="permanent"
        anchor="left"
      >
        <Toolbar />
        <Divider />{" "}
        <List>
          <ListItem>
            <Link to="/">Timeline</Link>
          </ListItem>
          <ListItem>
            <Link to="/follow">Follow</Link>
          </ListItem>
          <ListItem>
            <Link to="/post">Post</Link>
          </ListItem>
        </List>
      </Drawer>
    </Box>
  );
};

export default Sidebar;
