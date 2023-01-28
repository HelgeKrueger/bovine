import React from "react";
import { createHashRouter } from "react-router-dom";
import Followers from "./pages/Followers";
import Main from "./pages/Main";
import Post from "./pages/Post";
import Timeline from "./pages/Timeline";

const router = createHashRouter([
  {
    path: "/",
    element: <Main />,
    children: [
      {
        path: "/",
        element: <Timeline />,
      },
      {
        path: "/follow",
        element: <Followers />,
      },
      {
        path: "/post",
        element: <Post />,
      },
    ],
  },
]);

export default router;
