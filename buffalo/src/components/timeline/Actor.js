import { Link } from "@mui/material";
import React from "react";

const Actor = ({ name }) => {
  const hostname = new URL(name).hostname;
  const pieces = name.split("/");
  const username = pieces[pieces.length - 1];

  return (
    <Link href={name} target="_blank">
      <b>{username}</b>@{hostname}
    </Link>
  );
};

export default Actor;
