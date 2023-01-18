import * as esbuild from "esbuild";
import http from "node:http";

let ctx = await esbuild.context({});

let { host, port } = await ctx.serve({ port: 8001, servedir: "." });
console.log(host, port);

http
  .createServer((req, res) => {
    console.log(req.url);
    if (req.url.startsWith("/api")) {
      const options = {
        hostname: "localhost",
        port: 8000,
        path: req.url.replace("/api", ""),
        method: req.method,
        headers: req.headers,
      };

      // Forward each incoming request to esbuild
      const proxyReq = http.request(options, (proxyRes) => {
        res.writeHead(proxyRes.statusCode, proxyRes.headers);
        proxyRes.pipe(res, { end: true });
      });

      // Forward the body of the request to esbuild
      req.pipe(proxyReq, { end: true });
    } else {
      const options = {
        hostname: host,
        port: port,
        path: req.url,
        method: req.method,
        headers: req.headers,
      };

      // Forward each incoming request to esbuild
      const proxyReq = http.request(options, (proxyRes) => {
        res.writeHead(proxyRes.statusCode, proxyRes.headers);
        proxyRes.pipe(res, { end: true });
      });

      // Forward the body of the request to esbuild
      req.pipe(proxyReq, { end: true });
    }
  })
  .listen(3000);
