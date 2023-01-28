import { Button, Paper, Typography } from "@mui/material";
import React, { useRef, useState } from "react";
import { useNavigate } from "react-router";
import { Stage, Layer, Line } from "react-konva";
import { v4 as uuidv4 } from "uuid";
import { ArrowBack, Clear } from "@mui/icons-material";

function dataURItoBlob(dataURI, type) {
  var byteString = atob(dataURI.split(",")[1]);

  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }

  var bb = new Blob([ab], { type: type });
  return bb;
}

const Sketch = () => {
  const [lines, setLines] = useState([]);
  const isDrawing = useRef(false);
  const stageRef = React.useRef(null);

  const navigate = useNavigate();

  const sendPost = () => {
    const image = stageRef.current.toDataURL();
    console.log(image);

    const formData = new FormData();

    const imageName = "image";

    formData.append(imageName, dataURItoBlob(image, "image/png"), "image.png");

    fetch("http://localhost:5000/add", {
      method: "POST",
      body: formData,
    });

    // const note = buildNote(config.actor, content, {
    //   hashtags: hashtags.split(",").map((x) => x.trim()),
    // });
    // const data = buildCreateForNote(note);

    // sendToOutbox(data).then(() => {
    //   navigate("/");
    // });
  };

  const handleMouseDown = (e) => {
    isDrawing.current = true;
    const pos = e.target.getStage().getPointerPosition();
    setLines([...lines, { tool: "pen", points: [pos.x, pos.y] }]);
  };

  const handleMouseMove = (e) => {
    if (!isDrawing.current) {
      return;
    }
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    let lastLine = lines[lines.length - 1];
    lastLine.points = lastLine.points.concat([point.x, point.y]);
    lines.splice(lines.length - 1, 1, lastLine);
    setLines(lines.concat());
  };

  const handleMouseUp = () => {
    isDrawing.current = false;
  };

  return (
    <Paper sx={{ margin: 0, padding: 0 }} elevation={3}>
      <Typography variant="h3">New Sketch</Typography>
      <div>
        <Stage
          ref={stageRef}
          width={300}
          height={300}
          onMouseDown={handleMouseDown}
          onMousemove={handleMouseMove}
          onMouseup={handleMouseUp}
          onTouchStart={handleMouseDown}
          onTouchEnd={handleMouseUp}
          onTouchMove={handleMouseMove}
        >
          <Layer>
            {lines.map((line, i) => (
              <Line
                key={i}
                points={line.points}
                stroke="black"
                strokeWidth={5}
                tension={0.5}
                lineCap="round"
                lineJoin="round"
                globalCompositeOperation={"source-over"}
              />
            ))}
          </Layer>
        </Stage>
      </div>
      <Button onClick={sendPost} variant="contained" fullWidth>
        Post
      </Button>
      <Button
        onClick={() => {
          setLines([]);
        }}
        variant="contained"
        fullWidth
        startIcon={<Clear />}
      >
        Erase
      </Button>
      <Button
        onClick={() => {
          navigate("/");
        }}
        variant="contained"
        fullWidth
        startIcon={<ArrowBack />}
      >
        Back
      </Button>
    </Paper>
  );
};

export default Sketch;
