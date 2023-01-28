import { Link } from "@mui/material";
import React from "react";

const Actor = ({ name, short }) => {
  const hostname = new URL(name).hostname;
  const pieces = name.split("/");
  const username = pieces[pieces.length - 1];

  if (short) {
    return (
      <Link href={name} target="_blank">
        {username}
      </Link>
    );
  }

  return (
    <Link href={name} target="_blank">
      <b>{username}</b>@{hostname}
    </Link>
  );
};

export default Actor;
