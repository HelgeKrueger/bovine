import React from "react";
import { createHashRouter } from "react-router-dom";
import Followers from "./pages/Followers";
import Main from "./pages/Main";
import Post from "./pages/Post";
import Sketch from "./pages/Sketch";
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
      {
        path: "/sketch",
        element: <Sketch />,
      },
    ],
  },
]);

export default router;
