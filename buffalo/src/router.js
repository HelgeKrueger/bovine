import React from "react";
import { createHashRouter } from "react-router-dom";
import Configure from "./pages/Configure";
import Fetch from "./pages/Fetch";
import Followers from "./pages/Followers";
import Main from "./pages/Main";
import Mentions from "./pages/Mention";
import Outbox from "./pages/Outbox";
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
      {
        path: "/fetch",
        element: <Fetch />,
      },
      {
        path: "/mentions",
        element: <Mentions />,
      },
      {
        path: "/config",
        element: <Configure />,
      },
      { path: "/outbox", element: <Outbox /> },
    ],
  },
]);

export default router;
