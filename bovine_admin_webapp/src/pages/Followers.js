import { Container, Paper, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AddFollower from "../AddFollower";
import Actor from "../components/timeline/Actor";

const Followers = () => {
  const [follower, setFollower] = useState([]);
  const [following, setFollowing] = useState([]);

  useEffect(() => {
    fetch("/api/follow")
      .then((x) => x.json())
      .then((x) => {
        setFollower(x?.follower);
        setFollowing(x?.following);
      });
  }, []);

  return (
    <Container>
      <Paper elevation={3}>
        <Typography variant="h3">Follow</Typography>
        <Link to="/">Back</Link>
        <AddFollower />
        <Typography variant="h4">Followers</Typography>
        <ul>
          {follower.map((x) => (
            <li key={x}>
              <Actor name={x} />
            </li>
          ))}
        </ul>
        <Typography variant="h4">Following</Typography>
        <ul>
          {following.map((x) => (
            <li key={x}>
              <Actor name={x} />
            </li>
          ))}
        </ul>
      </Paper>
    </Container>
  );
};

export default Followers;
