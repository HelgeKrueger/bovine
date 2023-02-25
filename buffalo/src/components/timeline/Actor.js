import { Link } from "@mui/material";
import React from "react";

const Actor = ({ name, short }) => {
  let actorName = "";
  let username;
  let url;

  if (typeof name === "object" && "name" in name) {
    actorName = name["name"];
    username = name["preferredUsername"];
    url = name["id"];
  } else {
    if (Array.isArray(name)) {
      name = name[0].id;
    }

    if (typeof name === "object") {
      name = name?.id;
    }

    url = name;
    if (!name) {
      name = "unknown";
    }

    const pieces = name.split("/");
    username = pieces[pieces.length - 1];
  }
  const hostname = new URL(url).hostname;

  if (short) {
    if (actorName !== "") {
      return (
        <Link href={url} target="_blank">
          {actorName}
        </Link>
      );
    }
    return (
      <Link href={url} target="_blank">
        {username}
      </Link>
    );
  }

  if (actorName !== "") {
    return (
      <Link href={url} target="_blank">
        <b>{actorName}</b>:{" "}
        <small>
          <b>{username}</b>@{hostname}
        </small>
      </Link>
    );
  }

  return (
    <Link href={url} target="_blank">
      <b>{username}</b>@{hostname}
    </Link>
  );
};

export default Actor;
