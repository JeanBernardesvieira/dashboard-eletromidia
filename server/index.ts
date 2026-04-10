import express from "express";
import { createServer } from "http";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const server = createServer(app);

  // Serve static files from dist/public in production
  const staticPath = path.resolve(__dirname, "..", "dist", "public");
  
  // Check if static path exists
  if (!fs.existsSync(staticPath)) {
    console.error(`Static path does not exist: ${staticPath}`);
    console.error(`Current directory: ${process.cwd()}`);
    console.error(`__dirname: ${__dirname}`);
    process.exit(1);
  }
  
  console.log(`Serving static files from: ${staticPath}`);

  app.use(express.static(staticPath));
  console.log(`Static files middleware configured`);

  // Handle client-side routing - serve index.html for all routes
  app.get("*", (_req, res) => {
    const indexPath = path.join(staticPath, "index.html");
    console.log(`Serving index.html from: ${indexPath}`);
    res.sendFile(indexPath, (err) => {
      if (err) {
        console.error("Error serving index.html:", err);
        res.status(404).send("Not Found");
      }
    });
  });

  const port = process.env.PORT || 3000;

  server.listen(port, "0.0.0.0", () => {
    console.log(`Server running on http://0.0.0.0:${port}/`);
    console.log(`Environment: ${process.env.NODE_ENV}`);
  });
}

startServer().catch((err) => {
  console.error("Failed to start server:", err);
  process.exit(1);
});
